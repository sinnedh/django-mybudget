# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import connection
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from models import Category, Expense, Tag
from forms import ExpenseFilterForm, ExpenseCreateInlineForm, ExpenseForm, CategoryForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out succesfully!'))
    return HttpResponseRedirect(redirect_to=reverse('login'))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "mybudget/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        account = self.request.user.account
        organisation = account.organisation

        context['data'] = []

        data = {'key': 'all', 'title': 'All accounts', 'active': True}
        data['sum'] = {}
        for days in [1, 7, 30, 90]:
            data['sum'][days] = Expense.objects.get_latest_sum(
                organisation=organisation, days=days) or 0
        data['last_expenses'] = Expense.objects.for_organisation(
            organisation=organisation)[:10]
        data['top_categories'] = {}
        for days in (7, 30, 90):
            data['top_categories'][days] = Expense.objects.summed_by_category(
                organisation=organisation, last_days=days)[:10]
        data['day_summary'] = []
        data['week_summary'] = []
        data['month_summary'] = []
        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = Expense.objects.for_organisation(
            organisation=organisation).extra({'month': truncate_date})
        month_summary = qs.values('month').annotate(Sum('amount'), Count('pk'))
        for i, m in enumerate(month_summary.order_by('-month')):
            """
            The database adaptors are behaving differently. For postgres a
            datetime object is returned, for sqlite a string is returned.
            """
            date = m['month']
            if type(m['month']) in [str, unicode]:
                date = datetime.datetime.strptime(m['month'], '%Y-%m-%d')
            data['month_summary'].append({'date': date,
                                          'amount_sum': m['amount__sum'],
                                          'count': m['pk__count']})
        context['data'].append(data)
        context['all_data'] = data

        for a in organisation.account_set.all():
            data = []
            data = {'key': 'user{}'.format(a.id), 'title': a.name, 'active': False}
            data['sum'] = {}
            for days in [1, 7, 30, 90]:
                data['sum'][days] = Expense.objects.get_latest_sum(
                    organisation=organisation, account=a, days=days) or 0
            data['last_expenses'] = Expense.objects.for_organisation(
                organisation=organisation, account=a)[:10]
            data['top_categories'] = {}
            for days in (7, 30, 90):
                data['top_categories'][days] = Expense.objects.summed_by_category(
                    organisation=organisation, account=a, last_days=days)[:10]
            data['day_summary'] = []
            data['week_summary'] = []
            data['month_summary'] = []
            truncate_date = connection.ops.date_trunc_sql('month', 'date')
            qs = Expense.objects.for_organisation(
                organisation=organisation, account=a).extra({'month': truncate_date})
            month_summary = qs.values('month').annotate(Sum('amount'), Count('pk'))
            for i, m in enumerate(month_summary.order_by('-month')):
                """
                The database adaptors are behaving differently. For postgres a
                datetime object is returned, for sqlite a string is returned.
                """
                date = m['month']
                if type(m['month']) in [str, unicode]:
                    date = datetime.datetime.strptime(m['month'], '%Y-%m-%d')
                data['month_summary'].append({'date': date,
                                              'amount_sum': m['amount__sum'],
                                              'count': m['pk__count']})
            if a.id == self.request.user.account.id:
                context['my_data'] = data
            context['data'].append(data)

        context['create_expense_form'] = ExpenseCreateInlineForm(organisation)
        context.update(csrf(self.request))

        return context


# TODO implement the filters from expenses !?!
class TagListView(LoginRequiredMixin, ListView):
    model = Tag

    def get_queryset(self):
        return Tag.objects.for_organisation(self.request.user.account.organisation)

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag_count'] = self.get_queryset().count()
        return context


# TODO validations
class TagFormViewMixin(LoginRequiredMixin):
    model = Tag
    fields = ['name', 'description', ]
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(TagFormViewMixin, self).form_valid(form)


class TagCreateView(TagFormViewMixin, CreateView):
    pass


class TagUpdateView(TagFormViewMixin, UpdateView):
    pass


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list')


# TODO implement the filters from expenses !?!
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self):
        return Category.objects.for_organisation(self.request.user.account.organisation)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category_count'] = self.get_queryset().count()
        return context


# TODO validations
class CategoryFormViewMixin(LoginRequiredMixin):
    model = Category
    fields = ['name', 'description', 'super_category', 'icon']
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryFormViewMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryFormViewMixin, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        return CategoryForm(self.request.user.account.organisation,
                            **self.get_form_kwargs())


class CategoryCreateView(CategoryFormViewMixin, CreateView):
    pass


class CategoryUpdateView(CategoryFormViewMixin, UpdateView):
    pass


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense

    def get_queryset(self):
        return Expense.objects.for_organisation(self.request.user.account.organisation)

    def get_context_data(self, **kwargs):
        organisation = self.request.user.account.organisation
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        context['expenses_sum'] = self.get_queryset().aggregate(
            expenses_sum=Sum('amount'))['expenses_sum']
        context['show_link_to_all_expenses'] = False
        context['expenses_count'] = self.get_queryset().count()
        initial = {}
        initial.update(self.request.REQUEST)
        context['filter_form'] = ExpenseFilterForm(organisation=organisation,
                                                   initial=initial)

        return context


class FilteredExpenseListView(ExpenseListView):
    def get_queryset(self):
        return Expense.objects.request_filter(
            organisation=self.request.user.account.organisation,
            request=self.request.REQUEST)



# TODO: merge with  FilteredExpenseListVIew
class LatestExpenseListView(ExpenseListView):
    model = Expense

    def get_queryset(self):
        all_expenses = self.request.user.account.organisation.get_latest_expenses(days=7)
        return all_expenses.order_by('-date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super(LatestExpenseListView, self).get_context_data(**kwargs)
        context['show_link_to_all_expenses'] = True
        return context


# TODO validations
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['date', 'amount', 'category', 'tags', 'is_shared', 'comment', ]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super(ExpenseCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ExpenseCreateView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        return ExpenseForm(self.request.user.account.organisation,
                           **self.get_form_kwargs())


# TODO validations
class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['date', 'amount', 'category', 'tags', 'is_shared', 'comment', ]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super(ExpenseUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ExpenseUpdateView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        return ExpenseForm(self.request.user.account.organisation,
                           **self.get_form_kwargs())


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
