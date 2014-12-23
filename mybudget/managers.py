# -*- coding: utf-8 -*-
import datetime

from django.db import models


class ExpenseManager(models.Manager):
    pass


class ExpenseForOrganisationManager(models.Manager):

    def for_organisation(self, organisation):
        queryset = self.get_queryset().filter(
            category__organisation=organisation)
        return queryset

    def get_queryset(self):
        return super(self.__class__, self).get_queryset().order_by(
            '-date', '-created_at')

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

    def get_latest(self, organisation, days=1):
        queryset = self.for_organisation(organisation)
        min_date = datetime.date.today() - datetime.timedelta(days=days)
        return queryset.filter(date__gt=min_date)


class CategoryManager(models.Manager):
    pass


class CategoryForOrganisationManager(models.Manager):

    def for_organisation(self, organisation):
        queryset = self.get_queryset().filter(organisation=organisation)
        return queryset

    def get_queryset(self):
        return super(self.__class__, self).get_queryset().order_by(
            'super_category__name', 'name')
