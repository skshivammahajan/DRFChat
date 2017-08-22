from django.conf.urls import url
from rest_framework import routers

from stats import views

router = routers.SimpleRouter()

router.register(r'tagstats', views.TagStatsViewSet, base_name='tagstats')

urlpatterns = [
    url(r'^me-stats/$', views.DailyExpertStatsView.as_view(), name='me-stats')
]

urlpatterns += router.urls
