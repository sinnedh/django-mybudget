# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Sum


class ExpenseManager(models.Manager):

    def get_queryset(self):
        return super(ExpenseManager, self).get_queryset().order_by(
            '-date', '-created_at')

    def _prefiltered_queryset(self, **kwargs):
        queryset = self.get_queryset()

        organisation = kwargs.get('organisation', None)
        if organisation is not None:
            queryset = queryset.filter(category__organisation=organisation)

        account = kwargs.get('account', None)
        if account is not None:
            queryset = queryset.filter(account=account)

        category = kwargs.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)

        is_shared = kwargs.get('is_shared', None)
        if is_shared is not None:
            queryset = queryset.filter(is_shared=is_shared)

        last_days = kwargs.get('last_days', None)
        if last_days is not None:
            enddate = datetime.date.today()
            startdate = enddate - datetime.timedelta(days=last_days)
        else:
            startdate = kwargs.get('startdate', None)
            enddate = kwargs.get('enddate', None)

        if startdate is not None:
            queryset = queryset.filter(date__gte=startdate)
        if enddate is not None:
            queryset = queryset.filter(date__lte=enddate)

        return queryset


class ExpenseForOrganisationManager(ExpenseManager):

    def for_account(self, account):
        # TODO test!
        queryset = self.get_queryset().filter(
            account=account)
        return queryset

    def for_organisation(self, organisation):
        queryset = self.get_queryset().filter(
            category__organisation=organisation)
        return queryset

    def request_filter(self, organisation, request):
        queryset = self.for_organisation(organisation)

        # filter for age_in_days
        filter_age_in_days = request.get('age_in_days', None)
        if filter_age_in_days:
            min_date = datetime.date.today() - datetime.timedelta(days=int(filter_age_in_days))
            queryset = queryset.filter(date__gt=min_date)

        # filter for category
        filter_category_id = request.get('category', None)
        if filter_category_id:
            # from models import Category
            # filter_category = Category.objects.get(pk=int(filter_category_id))
            #  TODO filter for all levels of subcategories here
            # all_sub_categories = filter_category.get_sub_categories()
            # qs = qs.filter(category_id__in=all_sub_categories)
            queryset = queryset.filter(category_id=filter_category_id)

        # filter for account
        filter_account_id = request.get('account', None)
        if filter_account_id:
            queryset = queryset.filter(account_id=int(filter_account_id))
        return queryset

    def get_latest(self, days=1, **kwargs):
        return self._prefiltered_queryset(last_days=days, **kwargs)

    def get_latest_sum(self, organisation, account=None, days=1):
        # TODO: test!
        if account is None:
            queryset = self.get_latest(organisation=organisation,
                                       days=days,
                                       is_shared=None)
            result = queryset.aggregate(amount_sum=Sum('amount'))['amount_sum']
            return result

        queryset = self.get_latest(organisation=organisation,
                                   account=account,
                                   days=days,
                                   is_shared=False)
        result = queryset.aggregate(amount_sum=Sum('amount'))['amount_sum']
        queryset_shared = self.get_latest(organisation=organisation,
                                          account=account,
                                          days=days,
                                          is_shared=True)
        result_shared = queryset_shared.aggregate(amount_sum=Sum('amount'))['amount_sum']
        if result_shared:
            return result + result_shared / organisation.account_set.count()
        return result

    def summed_by_category(self, **kwargs):
        queryset = self._prefiltered_queryset(**kwargs)
        return queryset.values('category_id', 'category__name').annotate(
            amount_sum=Sum('amount')).order_by('-amount_sum')

    def _prefiltered_queryset(self, organisation=None, **kwargs):
        if organisation is None:
            raise PermissionDenied('ExpenseForOrganisationManager requires use of "organisation"')
        return super(ExpenseForOrganisationManager, self)._prefiltered_queryset(organisation=organisation, **kwargs)



class CategoryManager(models.Manager):

    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().order_by(
            'super_category__name', 'name')


class CategoryForOrganisationManager(CategoryManager):

    def for_organisation(self, organisation):
        queryset = self.get_queryset().filter(organisation=organisation)
        return queryset



class TagManager(models.Manager):

    def get_queryset(self):
        return super(TagManager, self).get_queryset().order_by('name')


class TagForOrganisationManager(TagManager):

    def for_organisation(self, organisation):
        queryset = self.get_queryset().filter(
            organisation=organisation)
        return queryset
