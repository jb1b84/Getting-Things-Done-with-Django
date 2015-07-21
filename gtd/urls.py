from django.conf.urls import patterns, url
from gtd import views

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^page/add/$', views.PageCreateView.as_view(), name='page_add'),
    url(r'^page/(?P<slug>[-\w]+)/update/$', views.PageUpdateView.as_view(), name='page_update'),
    url(r'^page/(?P<slug>[-\w]+)/delete/$', views.PageDeleteView.as_view(), name='page_delete'),
    url(r'^page/(?P<slug>[-\w]+)/$', views.PageDetailView.as_view(), name='page_detail'),
    url(r'^task/add/$', views.TaskCreateView.as_view(), name='task_add'),
    url(r'^task/(?P<pk>\d+)/update/$', views.TaskUpdateView.as_view(), name='task_update'),
    url(r'^task/(?P<pk>\d+)/handle/(?P<action>[-\w]+)/$', views.handle_task, name='task_handle'),
    url(r'^task/(?P<pk>\d+)/upgrade/$', views.upgrade_task, name='task_upgrade'),
)