# -*- coding: utf-8 -*-
from django import forms

import models
import widgets


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
    account = forms.ModelChoiceField(queryset=models.Account.objects.none(), required=False)
    category = forms.ModelChoiceField(queryset=models.Category.objects.none(), required=False)

    class Meta:
        model = models.Expense
        fields = ['category', 'account']

    def __init__(self, organisation, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = models.Account.objects.filter(organisation=organisation)
        self.fields['category'].queryset = models.Category.objects.for_organisation(organisation)


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=widgets.BootstrapDateWidget)
    amount = forms.CharField(widget=widgets.BootstrapCurrencyWidget)
    comment = forms.CharField()

    class Meta:
        model = models.Expense
        fields = ['date', 'amount', 'category', 'tags', 'comment', 'is_shared']

    def __init__(self, organisation, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=models.Category.objects.for_organisation(organisation),
                                                         widget=widgets.CategorySelectWidget)

        self.fields['tags'].queryset = models.Tag.objects.for_organisation(organisation)
        self.fields['tags'].widget.attrs['class'] = 'selectpicker'
        self.fields['tags'].widget.attrs['title'] = 'Tags'
        self.fields['category'].widget.attrs['class'] = 'selectpicker'


class ExpenseCreateInlineForm(ExpenseForm):

    class Meta:
        model = models.Expense
        fields = ['date', 'amount', 'category', 'tags', 'comment']


class CategoryForm(forms.ModelForm):
    icon = forms.TypedChoiceField(widget=widgets.IconSelectWidget, choices=widgets.ICONS_CHOICES)

    class Meta:
        model = models.Category
        fields = ['name', 'description', 'super_category', 'icon']

    def __init__(self, organisation, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['super_category'].queryset = models.Category.objects.for_organisation(organisation)
        #import pdb; pdb.set_trace()  # XXX BREAKPOINT
        #self.fields['icon'].widget= widgets.IconListWidget()


