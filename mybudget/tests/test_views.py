# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from mybudget.models import Category, Expense, Tag
from mybudget.tests.base import BaseTests


class BaseViewTests(BaseTests):
    pass


class DashboardViewTests(BaseViewTests):
    def test_empty_dashboard(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class CategoryViewTests(BaseViewTests):
    def test_login_required_list(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/categories/')

    def test_login_required_update(self):
        # TODO: create category before ....
        response = self.client.get(reverse('category_update', args=(1, )))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/category/1/')

    def test_login_required_add(self):
        response = self.client.get(reverse('category_add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/category/add/')

    def test_login_required_delete(self):
        # TODO create before delete
        response = self.client.get(reverse('category_delete', args=(1, )))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/category/1/delete/')

    def test_list_empty(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        Category.objects.create(name='Test category', organisation=self.o1)
        Category.objects.create(name='Another test category', organisation=self.o1)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<td>Test category</td>')
        self.assertContains(response, '<td>Another test category</td>')

    def test_add(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Create Category</h2>')

    def test_update(self):
        c = Category.objects.create(name='Test category', organisation=self.o1)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_update', args=(c.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Update Category</h2>')


class ExpenseViewTests(BaseViewTests):
    def test_list_empty(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        c = Category.objects.create(name='Test category', organisation=self.o1)
        Expense.objects.create(comment='Test expense', account=self.a1, category=c)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test expense')
        self.assertContains(response, '<strong>Test category</strong>')

    def test_add(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('expense_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Create Expense</h2>')

    def test_update(self):
        c = Category.objects.create(name='Test category', organisation=self.o1)
        e = Expense.objects.create(comment='Test expense', account=self.a1, category=c)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('expense_update', args=(e.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Update Expense</h2>')


class TagViewTests(BaseViewTests):
    def test_list_empty(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('tag_list'))
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        Tag.objects.create(name='Test tag', organisation=self.o1)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<td>Test tag</td>')

    def test_add(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('tag_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Create Tag</h2>')

    def test_update(self):
        t = Tag.objects.create(name='Test tag', organisation=self.o1)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('tag_update', args=(t.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Update Tag</h2>')
