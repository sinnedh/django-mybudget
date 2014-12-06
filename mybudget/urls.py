# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

from mybudget.views import DashboardView
from mybudget.views import (ExpenseListView,
                            ExpenseCreateView,
                            ExpenseUpdateView,
                            ExpenseDeleteView,
                            FilteredExpenseListView,
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

    url(r'^$', DashboardView.as_view(), name='start'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^expenses/latest/$', LatestExpenseListView.as_view(), name='latest_expense_list'),
    url(r'^expenses/$', FilteredExpenseListView.as_view(), name='expense_list'),
    url(r'^expense/add/$', ExpenseCreateView.as_view(), name='expense_add'),
    url(r'^expense/(?P<pk>[0-9]+)/$', ExpenseUpdateView.as_view(), name='expense_update'),
    url(r'^expense/(?P<pk>[0-9]+)/details/$', ExpenseUpdateView.as_view(), name='expense_details'),
    url(r'^expense/(?P<pk>[0-9]+)/delete/$', ExpenseDeleteView.as_view(), name='expense_delete'),

    url(r'^categories/$', CategoryListView.as_view(), name='category_list'),
    url(r'^categories/add/$', CategoryCreateView.as_view(), name='category_add'),
    url(r'^category/(?P<pk>[0-9]+)/details/$', CategoryUpdateView.as_view(), name='category_details'),
    url(r'^category/(?P<pk>[0-9]+)/delete/$', CategoryDeleteView.as_view(), name='category_delete'),
)
