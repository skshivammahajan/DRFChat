from django.conf.urls import url

from cms import views

urlpatterns = [
    url(r'^superusers/$', views.SuperUserView.as_view(), name='superuser-list'),
    url(r'^superusers/(?P<pk>\d+)/enable/$', views.SuperUserEnableView.as_view(), name='superuser-enable'),
    url(r'^superusers/(?P<pk>\d+)/disable/$', views.SuperUserDisableView.as_view(), name='superuser-disable'),
]
