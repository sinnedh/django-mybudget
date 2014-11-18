# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


#class BaseModel(models.Model):
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)


class Organisation(models.Model):
    class Meta:
        verbose_name = _('Organisation')
        verbose_name_plural = _('Organisation')

    name = models.TextField(_('name'))
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    organisation = models.ForeignKey(Organisation)
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    super_category = models.ForeignKey('self', null=True, blank=True, default=None)
    organisation = models.ForeignKey(Organisation)
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return self.name

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


class Expense(models.Model):
    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    category = models.ForeignKey(Category)
    account = models.ForeignKey(Account)

    date = models.DateField(_('date'), default=datetime.date.today)
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=10, default=0.00)
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __unicode__(self):
        return '{} Euro ({})'.format(self.amount, self.date)
