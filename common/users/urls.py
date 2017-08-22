from django.conf.urls import url
from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register(r'usermedia', views.UserMediaViewSet, base_name='usermedia')
router.register(r'expertprofiles', views.ExpertProfileView, base_name='expertprofile')
router.register(r'expert-accounts', views.ExpertAccountViewSet, base_name='expert-accounts')
router.register(r'slots', views.CalendarViewSet, base_name='slots')
router.register(r'promo-codes', views.PromoCodeViewSet, base_name='promo-code')


urlpatterns = [
    url(r'^me-basic-info/$', views.BasicInfoView.as_view(), name='me-basic-info'),
    url(r'^me-photo/$', views.PhotoUploadView.as_view(), name='me-photo-upload'),
    url(r'^phonecodesend/$', views.PhoneCodeSendView.as_view(), name='phonecodesend'),
    url(r'^phonecodeverify/$', views.PhoneVerifyView.as_view(), name='phonecodeverify'),
    url(r'^resendphonecode/$', views.ResendPhoneCodeSendView.as_view(), name='resendphonecode'),
    url(r'^profile/(?P<pk>[0-9]+)/social-links/$',
        views.ExpertProfileSocialLinksListView.as_view(),
        name='expert-profile-links'),
    url(r'^profile-status/$', views.ProfileStatusView.as_view(), name='profile-status'),
    url(r'^available-slots/(?P<expert_id>[0-9]+)/$', views.ExpertAppointmentsView.as_view(), name='expert-slots'),
    url(r'^(?P<condition_type>privacy_policy|toc)/$', views.TermsAndPolicyView.as_view(),
        name='toc-and-privacy-policy'),
    url(r'^(?P<condition_type>privacy_policy|toc)/send-mail/$',
        views.TermsAndPolicySendMailView.as_view(), name='toc-and-privacy-policy-send-email'),
    url(r'^experts/(?P<pk>[0-9]+)/reviews/$', views.SessionReviewView.as_view(), name='expert-session-reviews'),
    url(r'^accept-toc/$', views.TermsAndPolicyAcceptView.as_view(), name='accept-toc'),
    url(r'^follow/(?P<expert_id>[0-9]+)/$', views.FollowExpertView.as_view(), name='follow-expert'),
    url(r'^unfollow/(?P<expert_id>[0-9]+)/$', views.UnFollowExpertView.as_view(), name='unfollow-expert'),
    url(r'^me-following/$', views.UserFollowingExpertListView.as_view(), name='me-following'),
    url(r'^me-followers/$', views.ExpertFollowedByListView.as_view(), name='me-followers'),
    url(r'^following-tags/$', views.FollowTagsView.as_view(), name='following-tags'),
    url(r'^notification-settings/$', views.ExpertNotificationSettingsView.as_view(), name='notification-settings'),
    url(r'^super-featured-experts/$', views.SuperAdminFeaturedExpertsView.as_view(), name='super-featured-experts'),
    url(r'^user-featured-experts/$', views.FeaturedExpertsListView.as_view(), name='user-featured-experts'),
    url(r'^expert-profiles/$', views.ExpertProfileList.as_view(), name='expert-profile-list'),
    url(r'^expert-profiles/(?P<pk>[0-9]+)/$', views.ExpertProfileDetail.as_view(),
        name='expert-profile-detail'),
]

urlpatterns += router.urls
