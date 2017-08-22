from django.conf.urls import url
from rest_framework import routers

from search import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'experts/$', views.ExpertProfileView.as_view(), name='expert-list'),
    url(r'experts/(?P<pk>[0-9]+)/$', views.ExpertProfileDetailView.as_view(), name='expert-detail'),
    url(r'experts/random/$', views.ExpertRandomListView.as_view(), name='random-experts'),
    url(r'tags/$', views.TagView.as_view(), name='tag-list'),
]
