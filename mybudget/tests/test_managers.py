# -*- coding: utf-8 -*-
import datetime

from base import BaseTests
from mybudget.models import Expense, Category


class CategoryManagerTests(BaseTests):
    pass


class CategoryForOrganisationManagerTests(BaseTests):

    def test_for_organisation(self):
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o1)
        c3 = Category.objects.create(name='c3', organisation=self.o1)
        c4 = Category.objects.create(name='c4', organisation=self.o2)

        self.assertItemsEqual(Category.objects.for_organisation(self.o1),
                              [c1, c2, c3])
        self.assertItemsEqual(Category.objects.for_organisation(self.o2),
                              [c4])


class ExpenseManagerTests(BaseTests):
    pass


class TenantExpenseForOrganisationManagerTests(BaseTests):

    def _today_minus_n(self, n=0):
        return datetime.date.today() - datetime.timedelta(days=n)

    def test_for_organisation(self):
        today = self._today_minus_n()
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o2)

        e1a = Expense.objects.create(category=c1, account=self.a1, amount=34.56, date=today)
        e1b = Expense.objects.create(category=c1, account=self.a1, amount=77.01, date=today)
        e1c = Expense.objects.create(category=c1, account=self.a1, amount=20.22, date=today)

        e2a = Expense.objects.create(category=c2, account=self.a3, amount=34.56, date=today)
        e2b = Expense.objects.create(category=c2, account=self.a3, amount=44.23, date=today)


        self.assertItemsEqual(Expense.objects.for_organisation(self.o1),
                              [e1a, e1b, e1c])
        self.assertItemsEqual(Expense.objects.for_organisation(self.o2),
                              [e2a, e2b])


    def test_get_latest_expenses(self):
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o2)

        e1a = Expense.objects.create(category=c1, account=self.a1, amount=34.56, date=self._today_minus_n(0))
        e1b = Expense.objects.create(category=c1, account=self.a1, amount=77.01, date=self._today_minus_n(3))
        e1c = Expense.objects.create(category=c1, account=self.a1, amount=20.22, date=self._today_minus_n(21))

        e2a = Expense.objects.create(category=c2, account=self.a3, amount=34.56, date=self._today_minus_n(2))
        e2b = Expense.objects.create(category=c2, account=self.a3, amount=44.23, date=self._today_minus_n(5))


        self.assertItemsEqual(Expense.objects.get_latest(self.o1, 1),
                              [e1a])
        self.assertItemsEqual(Expense.objects.get_latest(self.o1, 3),
                              [e1a])
        self.assertItemsEqual(Expense.objects.get_latest(self.o1, 4),
                              [e1a, e1b])
        self.assertItemsEqual(Expense.objects.get_latest(self.o1, 5),
                              [e1a, e1b])
        self.assertItemsEqual(Expense.objects.get_latest(self.o1, 30),
                              [e1a, e1b, e1c])
        self.assertItemsEqual(Expense.objects.get_latest(self.o2, 2),
                              [])
        self.assertItemsEqual(Expense.objects.get_latest(self.o2, 6),
                              [e2a, e2b])

