from django.conf.urls import url

from domains import views

urlpatterns = [
    url(r'^domains/(?P<domain_id>[0-9]+)/tags/$', views.TagViewSet.as_view({'get': 'list'}), name="tags"),
]
