# -*- coding: utf-8 -*-

import datetime
import decimal

# from django.core.urlresolvers import reverse

from mybudget.tests.base import BaseTests
from mybudget.models import Category, Expense


class BaseModelTests(BaseTests):
    pass


class OrganisationModelTests(BaseModelTests):
    def test_get_latest_expenses(self):
        today = datetime.date.today()
        c1 = Category.objects.create(name='A category', organisation=self.o1)
        e1_1 = Expense.objects.create(date=today-datetime.timedelta(days=2),
                                      account=self.a1, category=c1, amount=1.1)
        e1_2 = Expense.objects.create(date=today-datetime.timedelta(days=31),
                                      account=self.a1, category=c1, amount=1.2)
        e1_3 = Expense.objects.create(date=today-datetime.timedelta(days=6),
                                      account=self.a1, category=c1, amount=1.3)
        e1_4 = Expense.objects.create(date=today-datetime.timedelta(days=8),
                                      account=self.a2, category=c1, amount=1.4)
        self.assertItemsEqual(self.o1.get_latest_expenses(days=32), [e1_1, e1_2, e1_3, e1_4])
        self.assertItemsEqual(self.o1.get_latest_expenses(days=7), [e1_1, e1_3])
        self.assertItemsEqual(self.o1.get_latest_expenses(days=3), [e1_1])
        self.assertItemsEqual(self.o1.get_latest_expenses(days=1), [])
        self.assertItemsEqual(self.o1.get_latest_expenses(days=0), [])

    def test_get_expenses(self):
        c1 = Category.objects.create(name='A category', organisation=self.o1)
        c2 = Category.objects.create(name='Another category', organisation=self.o2)
        e1_1 = Expense.objects.create(account=self.a1, category=c1, amount=1.1)
        e1_2 = Expense.objects.create(account=self.a1, category=c1, amount=1.2)
        e1_3 = Expense.objects.create(account=self.a1, category=c1, amount=1.3)
        e1_4 = Expense.objects.create(account=self.a2, category=c1, amount=1.4)
        e2_1 = Expense.objects.create(account=self.a3, category=c2, amount=2.1)
        e2_2 = Expense.objects.create(account=self.a3, category=c2, amount=2.2)
        e2_3 = Expense.objects.create(account=self.a4, category=c2, amount=2.3)
        self.assertEqual(self.o1.get_expenses().count(), 4)
        self.assertEqual(self.o2.get_expenses().count(), 3)
        self.assertItemsEqual(self.o1.get_expenses(), [e1_1, e1_2, e1_3, e1_4])
        self.assertItemsEqual(self.o2.get_expenses(), [e2_1, e2_2, e2_3])


class CategoryModelTests(BaseModelTests):
    def test_get_expense_sum(self):
        c = Category.objects.create(name='Category 1', organisation=self.o1)
        Expense.objects.create(comment='Expense 1',
                               account=self.a1,
                               date=datetime.date(2014, 11, 11),
                               amount=99.99,
                               category=c)
        self.assertEqual(c.get_expense_sum(), decimal.Decimal('99.99'))
        Expense.objects.create(comment='Expense 2',
                               account=self.a1,
                               date=datetime.date(2014, 11, 12),
                               amount=33.31,
                               category=c)
        self.assertEqual(c.get_expense_sum(), decimal.Decimal('133.30'))

    def test_get_expense_sum_for_empty_category(self):
        c = Category.objects.create(name='Category 1', organisation=self.o1)
        self.assertEqual(c.get_expense_sum(), 0.0)

    def test_get_expense_sum_for_empty_category_with_empty_sub_categories(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        self.assertEqual(category.get_expense_sum(), 0.0)
        sub_category1 = Category.objects.create(name='Category 1',
                                                organisation=self.o1,
                                                super_category=category)
        sub_category2 = Category.objects.create(name='Category 2',
                                                organisation=self.o1,
                                                super_category=category)
        self.assertEqual(sub_category1.get_expense_sum(), 0.0)
        self.assertEqual(sub_category2.get_expense_sum(), 0.0)
        self.assertEqual(category.get_expense_sum(), 0.0)

    def test_get_expense_sum_for_category_with_sub_categories(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=11.11,
                                          category=category)
        self.assertEqual(category.get_expense_sum(),
                         decimal.Decimal('11.11'))
        sub_category1 = Category.objects.create(name='Category 1',
                                                organisation=self.o1,
                                                super_category=category)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=99.99,
                                          category=sub_category1)
        self.assertEqual(sub_category1.get_expense_sum(),
                         decimal.Decimal('99.99'))
        self.assertEqual(category.get_expense_sum(),
                         decimal.Decimal('11.11'))
        sub_category2 = Category.objects.create(name='Category 2',
                                                organisation=self.o1,
                                                super_category=category)
        expense2 = Expense.objects.create(comment='Expense 2',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=22.23,
                                          category=sub_category2)
        expense2 = Expense.objects.create(comment='Expense 3',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=11.10,
                                          category=sub_category2)
        self.assertEqual(sub_category1.get_expense_sum(),
                         decimal.Decimal('99.99'))
        self.assertEqual(sub_category2.get_expense_sum(),
                         decimal.Decimal('33.33'))
        self.assertEqual(category.get_expense_sum(),
                         decimal.Decimal('11.11'))

    def test_get_expense_sum_for_empty_category_with_sub_categories(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        self.assertEqual(category.get_expense_sum(),
                         decimal.Decimal('0.00'))
        sub_category = Category.objects.create(name='Category 1',
                                               organisation=self.o1,
                                               super_category=category)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=99.99,
                                          category=sub_category)
        self.assertEqual(sub_category.get_expense_sum(),
                         decimal.Decimal('99.99'))

    def test_get_total_expense_sum(self):
        c = Category.objects.create(name='Category 1', organisation=self.o1)
        Expense.objects.create(comment='Expense 1',
                               account=self.a1,
                               date=datetime.date(2014, 11, 11),
                               amount=99.99,
                               category=c)
        self.assertEqual(c.get_total_expense_sum(), decimal.Decimal('99.99'))
        Expense.objects.create(comment='Expense 2',
                               account=self.a1,
                               date=datetime.date(2014, 11, 12),
                               amount=33.31,
                               category=c)
        self.assertEqual(c.get_total_expense_sum(), decimal.Decimal('133.30'))

    def test_get_total_expense_sum_for_empty_category(self):
        c = Category.objects.create(name='Category 1', organisation=self.o1)
        self.assertEqual(c.get_total_expense_sum(), 0.0)

    def test_get_total_expense_sum_for_empty_category_with_empty_sub_categories(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        self.assertEqual(category.get_total_expense_sum(), 0.0)
        sub_category1 = Category.objects.create(name='Category 1',
                                                organisation=self.o1,
                                                super_category=category)
        sub_category2 = Category.objects.create(name='Category 2',
                                                organisation=self.o1,
                                                super_category=category)
        self.assertEqual(sub_category1.get_total_expense_sum(), 0.0)
        self.assertEqual(sub_category2.get_total_expense_sum(), 0.0)
        self.assertEqual(category.get_total_expense_sum(), 0.0)

    def test_get_total_expense_sum_for_category_with_sub_category(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=11.11,
                                          category=category)
        self.assertEqual(category.get_total_expense_sum(),
                         decimal.Decimal('11.11'))
        sub_category1 = Category.objects.create(name='Category 1',
                                                organisation=self.o1,
                                                super_category=category)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=99.99,
                                          category=sub_category1)
        self.assertEqual(sub_category1.get_total_expense_sum(),
                         decimal.Decimal('99.99'))
        self.assertEqual(category.get_total_expense_sum(),
                         decimal.Decimal('111.10'))

        sub_category2 = Category.objects.create(name='Category 2',
                                                organisation=self.o1,
                                                super_category=category)
        expense2 = Expense.objects.create(comment='Expense 2',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=22.23,
                                          category=sub_category2)
        expense2 = Expense.objects.create(comment='Expense 3',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=11.10,
                                          category=sub_category2)
        self.assertEqual(sub_category1.get_total_expense_sum(),
                         decimal.Decimal('99.99'))
        self.assertEqual(sub_category2.get_total_expense_sum(),
                         decimal.Decimal('33.33'))
        self.assertEqual(category.get_total_expense_sum(),
                         decimal.Decimal('144.43'))

    def test_get_total_expense_sum_for_empty_category_with_sub_categories(self):
        category = Category.objects.create(name='Super Category',
                                           organisation=self.o1)
        self.assertEqual(category.get_total_expense_sum(),
                         decimal.Decimal('0.00'))
        sub_category = Category.objects.create(name='Category 1',
                                               organisation=self.o1,
                                               super_category=category)
        expense1 = Expense.objects.create(comment='Expense 1',
                                          account=self.a1,
                                          date=datetime.date(2014, 11, 11),
                                          amount=99.99,
                                          category=sub_category)
        self.assertEqual(sub_category.get_total_expense_sum(),
                         decimal.Decimal('99.99'))
        self.assertEqual(category.get_total_expense_sum(),
                         decimal.Decimal('99.99'))
