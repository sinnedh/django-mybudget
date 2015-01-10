# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

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


class ExpenseForOrganisationManagerTests(BaseTests):

    def test_summed_by_category(self):
        today = self._today_minus_n()
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o1)
        c3 = Category.objects.create(name='c3', organisation=self.o2)

        e1a = Expense.objects.create(category=c1, account=self.a1, amount=34.56, date=today)
        e1b = Expense.objects.create(category=c1, account=self.a1, amount=77.01, date=today)
        e1c = Expense.objects.create(category=c1, account=self.a1, amount=20.22, date=today)

        e2a = Expense.objects.create(category=c2, account=self.a2, amount=34.56, date=today)
        e2b = Expense.objects.create(category=c2, account=self.a2, amount=44.23, date=today)

        e2b = Expense.objects.create(category=c3, account=self.a3, amount=44.23, date=today)

        categories = Expense.objects.summed_by_category(organisation=self.o1)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0], {'category_id': c1.id,
                                         'category__name': 'c1',
                                         'amount_sum': Decimal('131.79')})
        self.assertEqual(categories[1], {'category_id': c2.id,
                                         'category__name': 'c2',
                                         'amount_sum': Decimal('78.79')})

        categories = Expense.objects.summed_by_category(organisation=self.o2)
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0], {'category_id': c3.id,
                                         'category__name': 'c3',
                                         'amount_sum': Decimal('44.23')})

    def _today_minus_n(self, n=0):
        return datetime.date.today() - datetime.timedelta(days=n)

    def test_for_account(self):
        # TODO
        pass

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

    def test_get_latest(self):
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o2)

        e1a = Expense.objects.create(category=c1, account=self.a1, amount=34.56,
                                     date=self._today_minus_n(0))
        e1b = Expense.objects.create(category=c1, account=self.a1, amount=77.01,
                                     date=self._today_minus_n(3))
        e1c = Expense.objects.create(category=c1, account=self.a1, amount=20.22,
                                     date=self._today_minus_n(21))

        e2a = Expense.objects.create(category=c2, account=self.a3, amount=34.56,
                                     date=self._today_minus_n(2))
        e2b = Expense.objects.create(category=c2, account=self.a3, amount=44.23,
                                     date=self._today_minus_n(5))

        expenses = Expense.objects.get_latest(organisation=self.o1, days=1)
        self.assertItemsEqual(expenses, [e1a])
        expenses = Expense.objects.get_latest(organisation=self.o1, days=3)
        self.assertItemsEqual(expenses, [e1a])
        expenses = Expense.objects.get_latest(organisation=self.o1, days=4)
        self.assertItemsEqual(expenses, [e1a, e1b])
        expenses = Expense.objects.get_latest(organisation=self.o1, days=30)
        self.assertItemsEqual(expenses, [e1a, e1b, e1c])

        expenses = Expense.objects.get_latest(organisation=self.o2, days=1)
        self.assertItemsEqual(expenses, [])
        expenses = Expense.objects.get_latest(organisation=self.o2, days=3)
        self.assertItemsEqual(expenses, [e2a])
        expenses = Expense.objects.get_latest(organisation=self.o2, days=6)
        self.assertItemsEqual(expenses, [e2a, e2b])

    def test_get_latest_with_account(self):
        c1 = Category.objects.create(name='c1', organisation=self.o1)
        c2 = Category.objects.create(name='c2', organisation=self.o1)

        e1a = Expense.objects.create(category=c1, account=self.a1, amount=34.56,
                                     date=self._today_minus_n(0))
        e1b = Expense.objects.create(category=c1, account=self.a1, amount=77.01,
                                     date=self._today_minus_n(3))
        e1c = Expense.objects.create(category=c1, account=self.a1, amount=20.22,
                                     date=self._today_minus_n(21))

        e2a = Expense.objects.create(category=c2, account=self.a2, amount=34.56,
                                     date=self._today_minus_n(3))
        e2b = Expense.objects.create(category=c2, account=self.a2, amount=44.23,
                                     date=self._today_minus_n(5))

        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a1, days=1)
        self.assertItemsEqual(expenses, [e1a])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a1, days=2)
        self.assertItemsEqual(expenses, [e1a])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a1, days=4)
        self.assertItemsEqual(expenses, [e1a, e1b])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a1, days=5)
        self.assertItemsEqual(expenses, [e1a, e1b])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a1, days=30)
        self.assertItemsEqual(expenses, [e1a, e1b, e1c])

        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a2, days=3)
        self.assertItemsEqual(expenses, [])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a2, days=4)
        self.assertItemsEqual(expenses, [e2a])
        expenses = Expense.objects.get_latest(organisation=self.o1, account=self.a2, days=6)
        self.assertItemsEqual(expenses, [e2a, e2b])

    def test_get_sum(self):
        # TODO
        pass

    def test_get_sum_with_account(self):
        # TODO
        pass
