from django.conf.urls import include, url

from api.v1 import views

urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^', include('search.urls')),
    url(r'^', include('stats.urls')),
]
