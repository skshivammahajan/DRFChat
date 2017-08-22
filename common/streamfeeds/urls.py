from django.conf.urls import url

from streamfeeds import views

urlpatterns = [
    url(r'^experts/(?P<expert_id>\d+)/feeds/$', views.ExpertFeedView.as_view(), name='expert-feed'),
    url(r'^tags/(?P<tag_id>\d+)/feeds/$', views.TagFeedFeedView.as_view(), name='tag-feed'),
    url(r'^expertprofiles/(?P<expert_profile_id>\d+)/feeds/$', views.ExpertProfileFeedView.as_view(),
        name='expert-profile-feed'),
    url(r'^superadmin/feeds/$', views.SuperAdminFeedView.as_view(), name='superadmin-feed'),
    url(r'^globaluser/feeds/$', views.GlobalUserFeedView.as_view(), name='user-global-feed'),
    url(r'^me-following-expert/feeds/$', views.FollowingExpertFeeds.as_view(), name='me-following-experts'),
    url(r'^me-following-tag/feeds/$', views.FollowingTagFeeds.as_view(), name='me-following-tags'),
    url(r'^user/aggregated-feeds/$', views.UserAggregatedTimelineFeeds.as_view(), name='user-aggregated-feeds'),
]
