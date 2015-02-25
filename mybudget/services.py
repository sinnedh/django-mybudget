# -*- coding: utf-8 -*-
import redis

from django.db.models import Sum, Count

from models import Expense


class CachingService(object):

    def __init__(self):
        # self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.redis = None

    def clear_for_organisation(self, organisation):
        if self.redis is None:
            return None
        keys = self.redis.keys('{}:*'.format(organisation))
        return len(keys)

    def get_cached_month_summary(self, year, month, organisation_id, account_id=None):
        if self.redis is None:
            return None
        sum = self.redis.get('{}:{}:{}_month_sum'.format(organisation_id, account_id or '', year, month))
        count = self.redis.get('{}:{}:{}_month_count'.format(organisation_id, account_id or '', year, month))
        if sum is not None and count is not None:
            return (count, sum)
        return None

    def cache_month_summary(self, count, sum, year, month, organisation_id, account_id=None):
        if self.redis is None:
            return None
        keyname = '{}:{}:{}_{}_month_sum'.format(organisation_id, account_id or '', year, month)
        self.redis.set(keyname, sum)

    def get_cached_expense_sum(self, days, organisation_id, account_id=None):
        if self.redis is None:
            return None
        keyname = '{}:{}:{}_sum'.format(organisation_id, account_id or '', days)
        sum = self.redis.get(keyname)
        return float(sum) if sum else None

    def cache_expense_sum(self, sum, days, organisation_id, account_id=None):
        if self.redis is None:
            return None
        keyname = '{}:{}:{}_sum'.format(organisation_id, account_id or '', days)
        self.redis.set(keyname, sum)
        self.redis.expire(keyname, 60)


class DashboardCachingService(CachingService):

    def month_summary(self, year, month, organisation, account=None):
        account_id = None
        if account:
            account_id = account.id
        month_summary = self.get_cached_month_summary(year, month, organisation.id, account_id)
        if month_summary is None:
            qs = Expense.objects.for_organisation(organisation=organisation, account=account).filter(
                date__month=month, date__year=year).aggregate(Sum('amount'), Count('pk'))
            """
            from django.db import connection
            truncate_date = connection.ops.date_trunc_sql('month', 'date')
            qs = Expense.objects.for_organisation(organisation=organisation).extra({'month': truncate_date}).filter()

            month_summary = qs.values('month').annotate(Sum('amount'), Count('pk'))
            for i, m in enumerate(month_summary.order_by('-month')):
                # The database adaptors are behaving differently. For postgres a
                # datetime object is returned, for sqlite a string is returned.
                date = m['month']
                if type(m['month']) in [str, unicode]:
                    date = datetime.datetime.strptime(m['month'], '%Y-%m-%d')
            """
            count = float(qs['pk__count'] or 0)
            sum = float(qs['amount__sum'] or 0)
            self.cache_month_summary(count, sum, year, month, organisation.id, account_id)
        else:
            (count, sum) = month_summary
        return (count, sum)

    def expenses_sum(self, days, organisation, account=None):
        account_id = None
        if account:
            account_id = account.id
        expense_sum = self.get_cached_expense_sum(days, organisation.id, account_id)
        if expense_sum is None:
            expense_sum = Expense.objects.get_latest_sum(organisation=organisation, days=days) or 0
            self.cache_expense_sum(expense_sum, days, organisation.id, account_id)
        return expense_sum
