# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from mybudget.models import Category, Expense, Tag
from mybudget.tests.base import BaseTests


class BaseViewTests(BaseTests):
    pass


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

    def test_list(self):
        Category.objects.create(name='Test category', organisation=self.o1)
        Category.objects.create(name='Another test category', organisation=self.o1)
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<td>Test category</td>')
        self.assertContains(response, '<td>Another test category</td>')
