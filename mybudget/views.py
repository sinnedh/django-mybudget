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


from models import Expense, Category
from forms import ExpenseFilterForm, ExpenseCreateInlineForm


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
        context['sum_today'] = organisation.get_latest_expenses(
            days=1).aggregate(expenses_sum=Sum('amount'))['expenses_sum']
        context['sum_7days'] = organisation.get_latest_expenses(
            days=7).aggregate(expenses_sum=Sum('amount'))['expenses_sum']
        context['sum_30days'] = organisation.get_latest_expenses(
            days=30).aggregate(expenses_sum=Sum('amount'))['expenses_sum']

        if context['sum_today'] is None:
            context['sum_today'] = 0
        if context['sum_7days'] is None:
            context['sum_7days'] = 0
        if context['sum_30days'] is None:
            context['sum_30days'] = 0

        context['last_expenses'] = organisation.get_expenses().order_by('-date', '-created_at')[:5]

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

        context['create_expense_form'] = ExpenseCreateInlineForm()
        context.update(csrf(self.request))
        return context


# TODO implement the filters from expenses !?!
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self):
        return self.request.user.account.organisation.category_set.all().order_by(
            'super_category__name', 'name')

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


# TODO validations
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'super_category', ]
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryUpdateView, self).form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense

    def get_queryset(self):
        all_expenses = self.request.user.account.organisation.get_expenses()
        return all_expenses.order_by('-date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        context['expenses_sum'] = self.get_queryset().aggregate(
            expenses_sum=Sum('amount'))['expenses_sum']
        context['show_link_to_all_expenses'] = False
        context['expenses_count'] = self.get_queryset().count()
        context['filter_form'] = ExpenseFilterForm(self.request.GET)

        return context


class FilteredExpenseListView(ExpenseListView):
    def get_queryset(self):
        qs = super(FilteredExpenseListView, self).get_queryset()

        # filter for age_in_days
        filter_age_in_days = self.request.REQUEST.get('age_in_days', None)
        if filter_age_in_days:
            # TODO: include this filter in the model (or better in a manager)
            min_date = datetime.date.today() - datetime.timedelta(days=int(filter_age_in_days))
            qs = qs.filter(date__gt=min_date)

        # filter for category
        filter_category = self.request.REQUEST.get('category', None)
        if filter_category:
            qs = qs.filter(category_id=int(filter_category))

        # filter for account
        filter_account = self.request.REQUEST.get('account', None)
        if filter_account:
            qs = qs.filter(account_id=int(filter_account))

        return qs


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
    fields = ['date', 'amount', 'category', 'is_shared', 'comment', ]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super(ExpenseCreateView, self).form_valid(form)


# TODO validations
class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['date', 'amount', 'category', 'is_shared', 'comment', ]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super(ExpenseUpdateView, self).form_valid(form)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
