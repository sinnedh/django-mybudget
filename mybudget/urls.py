# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

from mybudget.views import (ExpenseListView,
                            ExpenseCreateView,
                            ExpenseUpdateView,
                            ExpenseDeleteView,
                            LatestExpenseListView,)
from mybudget.views import (CategoryListView,
                            CategoryCreateView,
                            CategoryUpdateView,
                            CategoryDeleteView,)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mybudget.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/?$', 'django.contrib.auth.views.login', {
        'template_name': 'login.html'}, name='login'),
    url(r'^logout/?$', 'mybudget.views.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', ExpenseCreateView.as_view(), name='start'),
    url(r'^expenses/$', ExpenseListView.as_view(), name='expense_list'),
    url(r'^expenses/latest/$', LatestExpenseListView.as_view(), name='latest_expense_list'),
    url(r'^expense/add/$', ExpenseCreateView.as_view(), name='expense_add'),
    url(r'^expense/(?P<pk>[0-9]+)/$', ExpenseUpdateView.as_view(), name='expense_update'),
    url(r'^expense/(?P<pk>[0-9]+)/delete/$', ExpenseDeleteView.as_view(), name='expense_delete'),

    url(r'^categories/$', CategoryListView.as_view(), name='category_list'),
    url(r'^categories/add/$', CategoryCreateView.as_view(), name='category_add'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>[0-9]+)/delete/$', CategoryDeleteView.as_view(), name='category_delete'),
)
