# -*- coding: utf-8 -*-

import datetime
import decimal

# from django.core.urlresolvers import reverse

from mybudget.tests.base import BaseTests
from mybudget.models import Category, Expense


class BaseModelTests(BaseTests):
    pass


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
