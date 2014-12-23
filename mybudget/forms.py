# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from models import Account, Category, Expense, Tag


class BootstrapDateWidget(forms.widgets.DateInput):
    def render(self, name, value, attrs=None):
        attrs['data-provide'] = 'datepicker'
        html = ('<div class="input-group date">'
                '{}'
                '<span class="input-group-addon">'
                '<i class="glyphicon glyphicon-calendar"></i>'
                '</span>'
                '</div>')
        html = html.format(super(BootstrapDateWidget, self).render(name, value, attrs))
        return mark_safe(html)


class BootstrapCurrencyWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        html = ('<div class="input-group">'
                '{}'
                '<span class="input-group-addon">'
                '<i class="glyphicon glyphicon-euro"></i>'
                '</span>'
                '</div>')
        html = html.format(super(BootstrapCurrencyWidget, self).render(name, value, attrs))
        return mark_safe(html)


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


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=BootstrapDateWidget)
    date = forms.DateField(widget=BootstrapDateWidget)
    amount = forms.CharField(widget=BootstrapCurrencyWidget)
    comment = forms.CharField()

    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category', 'tags', 'comment', 'is_shared']

    def __init__(self, organisation, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.for_organisation(organisation)
        self.fields['tags'].queryset = Tag.objects.for_organisation(organisation)
        self.fields['tags'].widget.attrs['class'] = 'selectpicker'
        self.fields['tags'].widget.attrs['title'] = 'Tags'
        self.fields['category'].widget.attrs['class'] = 'selectpicker'


class ExpenseCreateInlineForm(ExpenseForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category', 'tags', 'comment']
