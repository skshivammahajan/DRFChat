from django.conf.urls import include, url

from api.v1 import views
from registration.views import PasswordResetConfirmView, VerifyEmailView

urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^(?P<user_type>expert|user)/$', views.ExpertUserApiRoot.as_view(), name='expertuser-api-root'),
    url(r'^(?P<user_type>expert|user)/', include('users.urls')),
    url(r'^(?P<user_type>expert|user)/', include('registration.urls')),
    url(r'^(?P<user_type>expert|user)/', include('feeds.urls')),
    url(r'^', include('feeds.urls')),
    url(r'^', include('domains.urls')),
    url(r'^', include('streamfeeds.urls')),
    url(r'^', include('users.urls')),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^verify/(?P<verification_token>'
        r'[0-9A-Za-z]{1,20}-[0-9A-Za-z]{1,20}-[0-9A-Za-z]{1,20}-[0-9A-Za-z]{1,20}-[0-9A-Za-z]{1,20})/$',
        VerifyEmailView.as_view(),
        name='verify_email'),
    url(r'^cms/$', views.CMSApiRoot.as_view(), name='cms-api-root'),
    url(r'^cms/', include('cms.urls')),
]
