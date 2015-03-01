from django.conf.urls import patterns, include, url
from django.contrib import admin

from mybudget import views


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mybudget.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/?$', 'django.contrib.auth.views.login', {
        'template_name': 'login.html'}, name='login'),
    url(r'^logout/?$', 'mybudget.views.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.DashboardView.as_view(), name='start'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    url(r'^expenses/latest/$', views.LatestExpenseListView.as_view(), name='latest_expense_list'),
    url(r'^expenses/$', views.FilteredExpenseListView.as_view(), name='expense_list'),
    url(r'^expenses/week/$', views.ExpenseCurrentWeekArchiveView.as_view(), name="expense_archive_week"),
    url(r'^expenses/week/(?P<year>\d{4})/(?P<week>\d+)/$', views.ExpenseWeekArchiveView.as_view(), name="expense_archive_week"),
    url(r'^expenses/month/$', views.ExpenseCurrentMonthArchiveView.as_view(), name="expense_archive_month"),
    url(r'^expenses/month/(?P<year>\d{4})/(?P<month>\d+)/$', views.ExpenseMonthArchiveView.as_view(), name="expense_archive_month"),

    url(r'^expense/add/$', views.ExpenseCreateView.as_view(), name='expense_add'),
    url(r'^expense/(?P<pk>[0-9]+)/$', views.ExpenseUpdateView.as_view(), name='expense_update'),
    url(r'^expense/(?P<pk>[0-9]+)/details/$', views.ExpenseUpdateView.as_view(), name='expense_details'),
    url(r'^expense/(?P<pk>[0-9]+)/delete/$', views.ExpenseDeleteView.as_view(), name='expense_delete'),

    url(r'^categories/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category/add/$', views.CategoryCreateView.as_view(), name='category_add'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>[0-9]+)/details/$', views.CategoryDetailView.as_view(), name='category_details'),
    url(r'^category/(?P<pk>[0-9]+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete'),

    url(r'^tags/$', views.TagListView.as_view(), name='tag_list'),
    url(r'^tag/add/$', views.TagCreateView.as_view(), name='tag_add'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagUpdateView.as_view(), name='tag_update'),
    url(r'^tag/(?P<pk>[0-9]+)/delete/$', views.TagDeleteView.as_view(), name='tag_delete'),
)
