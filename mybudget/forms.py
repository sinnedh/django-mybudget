# -*- coding: utf-8 -*-
from django import forms

from models import Expense, Category, Account

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


class ExpenseFilterForm(forms.Form):
    age_in_days = forms.ChoiceField(required=False, choices=FILTER_AGE_CHOICES)
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)

    class Meta:
        model = Expense
        fields = ['category', 'account']

    def __init__(self, organisation, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(organisation=organisation)
        self.fields['category'].queryset = Category.objects.for_organisation(organisation)


class ExpenseCreateInlineForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category', 'comment', 'is_shared']

    def __init__(self, organisation, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.for_organisation(organisation)
