# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import managers


class Organisation(models.Model):

    class Meta:
        verbose_name = _('Organisation')
        verbose_name_plural = _('Organisation')

    name = models.TextField(_('name'))
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def get_expenses(self):
        return Expense.objects.for_organisation(self)

    """
    def get_latest_expenses(self, days=1):
        min_date = datetime.date.today() - datetime.timedelta(days=days)
        return Expense.objects.all(self).filter(
            date__gt=min_date)
    """

    def __unicode__(self):
        return self.name


class Account(models.Model):

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    organisation = models.ForeignKey('Organisation')
    user = models.OneToOneField(User)
    color = models.CharField(_('Color'), max_length=32, null=True, blank=True, default='#3388CD')

    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def name(self):
        full_name = ' '.join((self.user.first_name, self.user.last_name))
        if full_name != ' ':
            return full_name
        return self.user.username

    def __unicode__(self):
        return self.user.username


class Category(models.Model):

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    all_objects = managers.CategoryManager()
    objects = managers.CategoryForOrganisationManager()

    super_category = models.ForeignKey('self', null=True, blank=True, default=None)
    organisation = models.ForeignKey('Organisation')
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('Icon'), max_length=32, null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def get_super_category_chain(self, chain=None):
        if chain is None:
            chain = []
        if self.super_category:
            self.super_category.get_super_category_chain(chain=chain)
        chain.append(self.name)
        return chain

    def __unicode__(self):
        return ' > '.join(self.get_super_category_chain())

    def get_expense_sum(self):
        # TODO: implement caching
        expense_sum = 0
        for e in self.expense_set.all():
            expense_sum += e.amount
        return expense_sum

    def get_total_expense_sum(self):
        """
        Includes all sub-categories
        """
        expense_sum = self.get_expense_sum()
        # sum over all sub categories
        for subcat in self.category_set.all():
            expense_sum += subcat.get_expense_sum()
        return expense_sum

    def get_sub_categories(self):
        return [c for c in self.category_set.all()]


class Tag(models.Model):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    all_objects = managers.TagManager()
    objects = managers.TagForOrganisationManager()

    organisation = models.ForeignKey('Organisation')
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return self.name


class Expense(models.Model):

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    all_objects = managers.ExpenseManager()
    objects = managers.ExpenseForOrganisationManager()

    tags = models.ManyToManyField('Tag', default=None, null=True, blank=True)
    category = models.ForeignKey('Category')
    account = models.ForeignKey('Account')

    date = models.DateField(_('date'), default=datetime.date.today)
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=10, default=0.00)
    comment = models.TextField(_('comment'), blank=True)
    is_shared = models.BooleanField(_('Is shared'), default=False)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return '{} Euro ({})'.format(self.amount, self.date)
