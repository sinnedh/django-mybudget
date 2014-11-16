# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organisation(models.Model):
    class Meta:
        verbose_name = _('Organisation')
        verbose_name_plural = _('Organisation')

    name = models.TextField(_('name'))
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    organisation = models.ForeignKey(Organisation)
    user = models.OneToOneField(User)

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

    def __unicode__(self):
        return self.name


class Expense(models.Model):
    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    category = models.ForeignKey(Category)
    account = models.ForeignKey(Account)

    date = models.DateField(_('date'))
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=10, default=0.00)
    comment = models.TextField(_('comment'), blank=True)

    def __unicode__(self):
        return '{} Euro ({})'.format(self.amount, self.date)
