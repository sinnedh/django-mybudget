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


from mybudget.models import Expense


# TODO login_required
# TODO filter for own expenses
class ExpenseListView(ListView):
    model = Expense

    queryset = Expense.objects.all()

# TODO login_required
# TODO validations
# TODO assign to user
class ExpenseCreateView(CreateView):
    model = Expense
    fields = ['date', 'amount', 'category', ]
    success_url = reverse_lazy('expense_list')

#    def form_valid(self, form):
#        form.instance.created_by = self.request.user
#        return super(AuthorCreate, self).form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['name']


#class ExpenseDeleteView(DeleteView):
#    model = Expense
#    success_url = reverse_lazy('expense-list')


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out succesfully!'))
    return HttpResponseRedirect(redirect_to=reverse('login'))
