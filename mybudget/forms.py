# -*- coding: utf-8 -*-
from django import forms

from models import Expense

class ExpenseFilterForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields =  ['category', 'account']
