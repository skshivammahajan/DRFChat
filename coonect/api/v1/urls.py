from django.conf.urls import include, url

from api.v1 import views

urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^', include('devices.urls')),
    url(r'^', include('experchat_sessions.urls')),
    url(r'^', include('notifications.urls')),
    url(r'^', include('payments.urls')),
]
