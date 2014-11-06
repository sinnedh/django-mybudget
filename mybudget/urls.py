from django.conf.urls import patterns, include, url
from django.contrib import admin

from mybudget.views import ExpenseListView, ExpenseCreateView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mybudget.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/?$', 'django.contrib.auth.views.login', {
        'template_name': 'login.html'}, name='login'),
    url(r'^logout/?$', 'mybudget.views.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^expenses/$', ExpenseListView.as_view(), name='expense_list'),
    url(r'^expense/add/$', ExpenseCreateView.as_view(), name='expense_add'),
#    url(r'^expense/(?P<pk>[0-9]+)/$', AuthorUpdate.as_view(), name='author_update'),
#    url(r'^expense/(?P<pk>[0-9]+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
)
