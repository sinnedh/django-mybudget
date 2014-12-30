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
        account = self.request.user.account
        organisation = account.organisation
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['sum_today'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                              account=account,
                                                              days=1) or 0
        context['sum_7days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                              account=account,
                                                              days=7) or 0
        context['sum_30days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                               account=account,
                                                               days=30) or 0
        context['sum_90days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                               account=account,
                                                               days=90) or 0

        if organisation.account_set.count() > 1:
            context['sum_all_today'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                                      days=1) or 0
            context['sum_all_7days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                                      days=7) or 0
            context['sum_all_30days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                                       days=30) or 0
            context['sum_all_90days'] = Expense.objects.get_latest_sum(organisation=organisation,
                                                                       days=90) or 0

        context['last_expenses'] = organisation.get_expenses().order_by('-date', '-created_at')[:10]

        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = organisation.get_expenses().extra({'month': truncate_date})
        month_summary_all = qs.values('month').annotate(Sum('amount'), Count('pk')).order_by('-month')
        context['day_summary'] = []
        context['week_summary'] = []
        context['month_summary'] = []
        for i, m_all in enumerate(month_summary_all):
            """
            The database adaptors are behaving differently. For postgres a datetime object is returned, for sqlite a
            string is returned.
            """
            date = m_all['month']
            if type(m_all['month']) in [str, unicode]:
                date = datetime.datetime.strptime(m_all['month'], '%Y-%m-%d')
            context['month_summary'].append({'date': date,
                                            'amount_sum': m_all['amount__sum'],
                                            'count': m_all['pk__count']})

        context['top_categories'] = {}
        for days in (7, 30, 90):
            context['top_categories'][days] = Expense.objects.summed_by_category(
                organisation=organisation,
                account=account,
                last_days=days)[:10]

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
class TagFormView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name', 'description', ]
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(TagFormView, self).form_valid(form)


class TagCreateView(TagFormView):
    pass


class TagUpdateView(LoginRequiredMixin, UpdateView):
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
class CategoryFormView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'super_category', 'icon']
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryFormView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        return CategoryForm(self.request.user.account.organisation,
                            **self.get_form_kwargs())


class CategoryCreateView(CategoryFormView):
    pass


class CategoryUpdateView(CategoryFormView):
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
