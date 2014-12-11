# -*- coding: utf-8 -*-
from django import forms

from models import Expense

FILTER_AGE_CHOICES = (
    ('', '---------'),
    ('1', 'Today'),
    ('3', 'Last 3 days'),
    ('7', 'Last 7 days'),
    ('14', 'Last 14 days'),
    ('30', 'Last 30 days'),
    ('90', 'Last 90 days'),
    ('180', 'Last 180 days'),
    ('360', 'Last 360days'),
)


class ExpenseFilterForm(forms.ModelForm):
    age_in_days = forms.ChoiceField(choices=FILTER_AGE_CHOICES)  # free input e.g. by PositiveIntegerField

    class Meta:
        model = Expense
        fields = ['category', 'account']


class ExpenseCreateInlineForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category', 'comment', 'is_shared']
