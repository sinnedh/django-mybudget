# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from mybudget.models import Expense, Category


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


# TODO filter for categories of own organisation
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    queryset = Expense.objects.all()


# TODO validations
# TODO assign to user
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['name', 'description',]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.organisation = self.request.user.account.organisation
        return super(CategoryCreateView, self).form_valid(form)


# TODO filter for own expenses
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    queryset = Expense.objects.all()


# TODO validations
# TODO assign to user
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['date', 'amount', 'category', ]
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super(ExpenseCreateView, self).form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['name']


#class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
#    model = Expense
#    success_url = reverse_lazy('expense-list')


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out succesfully!'))
    return HttpResponseRedirect(redirect_to=reverse('login'))
