from django.conf.urls import url
from rest_framework import routers

from feeds import views

router = routers.SimpleRouter()
router.register(r'social-links', views.SocialLinkViewSet, base_name='social_link')
router.register(r'contents', views.ContentViewSet, base_name='content')
router.register(r'super-admin-contents', views.SuperAdminContentViewSet, base_name='super-admin-content')
router.register(r'ignored-contents', views.IgnoredContentViewSet, base_name='ignored-content')

urlpatterns = [
    url(r'^feed/addlink/$', views.RSSLinkView.as_view(), name='feed-link'),
    url(r'^social/(?P<provider>[A-Za-z]+)/$', views.SocialUrlApiView.as_view(), name='social'),
    url(r'^social/(?P<provider>[A-Za-z]+)/get_token/(?P<app_code>[0-9A-Za-z_\-\/\\]+)/$',
        views.SocialUrlGetTokenView.as_view(), name='get_access_token'),
    url(r'^social/get_feeds/(?P<timestamp>[0-9]{1,13})/$', views.SocialAuthGetFeed.as_view(), name='get_feeds'),
]

urlpatterns += router.urls
