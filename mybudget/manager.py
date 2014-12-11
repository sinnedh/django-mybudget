# -*- coding: utf-8 -*-
import datetime

from django.db import models



class CategoryManager(models.Manager):

    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().order_by('super_category__name', 'name')

    def for_organisation(self, organisation):
        return self.get_queryset().filter(organisation=organisation)


class ExpenseManager(models.Manager):

    def get_queryset(self):
        return super(ExpenseManager, self).get_queryset().order_by('-date', '-created_at')

    def for_organisation(self, organisation):
        return self.get_queryset().filter(account__organisation=organisation)

    def request_filter(self, organisation, request):
        qs = self.for_organisation(organisation)

        # filter for age_in_days
        filter_age_in_days = request.get('age_in_days', None)
        if filter_age_in_days:
            min_date = datetime.date.today() - datetime.timedelta(days=int(filter_age_in_days))
            qs = qs.filter(date__gt=min_date)

        # filter for category
        filter_category_id = request.get('category', None)
        if filter_category_id:
            # from models import Category
            # filter_category = Category.objects.get(pk=int(filter_category_id))
            #  TODO filter for all levels of subcategories here
            # all_sub_categories = filter_category.get_sub_categories()
            # qs = qs.filter(category_id__in=all_sub_categories)
            qs = qs.filter(category_id=filter_category_id)

        # filter for account
        filter_account_id = request.get('account', None)
        if filter_account_id:
            qs = qs.filter(account_id=int(filter_account_id))

        return qs

