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
from forms import ExpenseFilterForm, ExpenseCreateInlineForm, ExpenseForm


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
        organisation = self.request.user.account.organisation
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['sum_today'] = Expense.objects.get_latest(organisation, 1).aggregate(
            expenses_sum=Sum('amount'))['expenses_sum']
        context['sum_7days'] = Expense.objects.get_latest(organisation, 7).aggregate(
            expenses_sum=Sum('amount'))['expenses_sum']
        context['sum_30days'] = Expense.objects.get_latest(organisation, 30).aggregate(
            expenses_sum=Sum('amount'))['expenses_sum']

        if context['sum_today'] is None:
            context['sum_today'] = 0
        if context['sum_7days'] is None:
            context['sum_7days'] = 0
        if context['sum_30days'] is None:
            context['sum_30days'] = 0

        context['last_expenses'] = organisation.get_expenses().order_by('-date', '-created_at')[:10]

        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = organisation.get_expenses().extra({'month': truncate_date})
        month_report = qs.values('month').annotate(Sum('amount'), Count('pk')).order_by('-month')
        context['month_report'] = []
        for m in month_report:
            """
            The database adaptors are behaving differently. For postgres a datetime object is returned, for sqlite a
            string is returned.
            """
            if type(m['month']) in [str, unicode]:
                date = datetime.datetime.strptime(m['month'], '%Y-%m-%d')
            else:
                date = m['month']
            context['month_report'].append({'sum': m['amount__sum'],
                                            'count': m['pk__count'],
                                            'date': date})

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
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name', 'description', ]
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(TagCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TagCreateView, self).get_context_data(**kwargs)
        return context


# TODO validations
class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name', 'description', ]
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(self.__class__, self).form_valid(form)


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
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'super_category', ]
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        return context


# TODO validations
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'super_category', ]
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        return context


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
