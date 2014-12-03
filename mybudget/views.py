# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from mybudget.models import Expense, Category


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out succesfully!'))
    return HttpResponseRedirect(redirect_to=reverse('login'))


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self):
        # TODO improve this query such that
        return self.request.user.account.organisation.category_set.all().order_by('super_category__name', 'name')


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
        context['show_link_to_all_expenses'] = False
        return context


class FilteredExpenseListView(ExpenseListView):
    def get_queryset(self):
        qs = super(FilteredExpenseListView, self).get_queryset()

        # filter for account
        filter_account = self.request.REQUEST.get('account', None)
        if filter_account is not None:
            qs = qs.filter(account_id=int(filter_account))

        # filter for category
        filter_category = self.request.REQUEST.get('category', None)
        if filter_category is not None:
            qs = qs.filter(category_id=int(filter_category))

        return qs


# TODO: merge with  FilteredExpenseListVIew
class LatestExpenseListView(LoginRequiredMixin, ListView):
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
