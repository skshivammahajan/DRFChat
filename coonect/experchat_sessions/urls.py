from django.conf.urls import url
from rest_framework import routers

from experchat_sessions import views

router = routers.SimpleRouter()

router.register(r'sessions', views.SessionViewSet, base_name='session')

urlpatterns = [
    url(r'^session-pricing/$', views.SessionPriceView.as_view(), name='session-pricing'),
    url(r'^(?P<session_type>past|future)-sessions/$', views.SessionListView.as_view(actions={'get': 'list'}),
        name='session-listing'),
    url(r'^sessions/(?P<pk>[0-9]+)/$',
        views.SessionListView.as_view(actions={'get': 'retrieve'}), name='session-detail'),
    url(r'^sessions/validate-promo-code/$', views.ValidatePromoCodeView.as_view(), name='validate-promo-code'),
]

urlpatterns += router.urls
