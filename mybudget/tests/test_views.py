# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from mybudget.models import Category
from mybudget.tests.base import BaseTests


class BaseViewTests(BaseTests):
    pass


class CategoryListViewTests(BaseViewTests):
    def test_not_logged_in(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/categories/')

    def test_logged_in(self):
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_with_existing_categries(self):
        return
        c1 = Category.objects.create(organisation=self.o1, name='Category 1')
        c2 = Category.objects.create(organisation=self.o1, name='Category 2')
        self.client.login(username=self.u1.username, password='password1')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.content, '''
            <table class="table table-striped">
                <tr>
                    <th></th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Super Category</th>
                </tr>

                <tr>
                    <td>
                        <a href="/category/1/">Edit</a> /
                        <a href="/category/1/delete/">Delete</a>
                    </td>
                    <td>Category 1</td>
                    <td></td>
                    <td>None</td>
                </tr>

                <tr>
                    <td>
                        <a href="/category/2/">Edit</a> /
                        <a href="/category/2/delete/">Delete</a>
                    </td>
                    <td>Category 2</td>
                    <td></td>
                    <td>None</td>
                </tr>

            </table>
            ''')

        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        #self.content
