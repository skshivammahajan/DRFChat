from collections import OrderedDict

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(['GET'])
def api_root(request, user_type=None):
    if not settings.ENABLE_API_ROOT:
        return Response(dict())

    if user_type is None:
        return Response(OrderedDict([
            ("Expert APIs", reverse('v1:expertuser-api-root', request=request, kwargs={'user_type': 'expert'})),
            ("User APIs", reverse('v1:expertuser-api-root', request=request, kwargs={'user_type': 'user'})),
            ("Common APIs", OrderedDict([
                ("Confirm password reset", reverse(
                    'v1:password_reset_confirm',
                    request=request,
                    kwargs={'uidb64': 'uid', 'token': 'reset-token'}
                )),
                ("Verify Email", reverse(
                    'v1:verify_email',
                    request=request,
                    kwargs={'verification_token': 'verify-email-sample-code-1'}
                )),
            ])),
            ("CMS APIs", reverse('v1:cms-api-root', request=request)),
        ]))


class ExpertUserApiRoot(APIView):
    def get(self, request, user_type):
        if not settings.ENABLE_API_ROOT:
            return Response(dict())

        return Response(OrderedDict([
            ("Registration APIs", OrderedDict([
                ("User registration", reverse('v1:user-registration', request=request,
                                              kwargs={'user_type': user_type})),
                ("Resend verification email", reverse('v1:resend_email', request=request,
                                                      kwargs={'user_type': user_type})),
                ("User login", reverse('v1:login', request=request, kwargs={'user_type': user_type})),
                ("Password Change", reverse('v1:password-change', request=request, kwargs={'user_type': user_type})),
                ("Password Reset", reverse('v1:rest_password_reset', request=request, kwargs={'user_type': user_type})),
            ])),
            ("Me APIs", OrderedDict([
                ("User Basic Info", reverse('v1:me-basic-info', request=request, kwargs={'user_type': user_type})),
                ("User Photo Upload", reverse('v1:me-photo-upload', request=request, kwargs={'user_type': user_type})),
                ("View Terms & Conditions", reverse('v1:toc-and-privacy-policy', request=request,
                                                    kwargs={'user_type': user_type, 'condition_type': 'toc'})),
                ("View Privacy Policy", reverse('v1:toc-and-privacy-policy', request=request,
                                                kwargs={'user_type': user_type, 'condition_type': 'privacy_policy'})),
                ("Email Privacy Policy", reverse('v1:toc-and-privacy-policy-send-email', request=request,
                                                 kwargs={'user_type': user_type, 'condition_type': 'privacy_policy'})),
                ("Email Terms & Conditions", reverse('v1:toc-and-privacy-policy-send-email', request=request,
                                                     kwargs={'user_type': user_type, 'condition_type': 'toc'})),
                ("Accept TOC", reverse('v1:accept-toc', request=request, kwargs={'user_type': user_type})),
            ])),
            ("Expert APIs", OrderedDict([
                ("Expert Profiles", reverse('v1:expertprofile-list', request=request, kwargs={'user_type': user_type})),
                ("Submit Expert Profile for Review", reverse('v1:expertprofile-submit-for-review', request=request,
                                                             kwargs={'user_type': user_type, 'pk': 1})),
                ("SuperAdmin Approve Expert Profile", reverse('v1:expertprofile-approve-profile', request=request,
                                                              kwargs={'user_type': user_type, 'pk': 1})),
                ("SuperAdmin Reject Expert Profile", reverse('v1:expertprofile-reject-profile', request=request,
                                                             kwargs={'user_type': user_type, 'pk': 1})),
                ("Expert social links", reverse('v1:expert-profile-links', request=request,
                                                kwargs={'user_type': user_type, 'pk': 1})),
                ("Expert Profile Review List ", reverse('v1:expert-profile-list', request=request,
                                                        kwargs={'user_type': user_type})),
                ("Expert Profile Review Detail ", reverse('v1:expert-profile-detail', request=request,
                                                          kwargs={'user_type': user_type, 'pk': 1})),
            ])),
            ("UserMedia APIs", OrderedDict([
                ("User Media Info", reverse('v1:usermedia-list', request=request, kwargs={'user_type': user_type})),
            ])),
            ("Phone APIs", OrderedDict([
                ("Phone Code Send", reverse('v1:phonecodesend', request=request, kwargs={'user_type': user_type})),
                ("Phone Code Verify", reverse('v1:phonecodeverify', request=request, kwargs={'user_type': user_type})),
                ("Phone Code Re-Send", reverse('v1:resendphonecode', request=request, kwargs={'user_type': user_type})),
            ])),
            ("Tags APIs", OrderedDict([
                ("Tags List", reverse('v1:tags', request=request, args=(1,))),
            ])),
            ("Feeds APIs", OrderedDict([
                ("Feed Link", reverse('v1:feed-link', request=request)),
                ("Social", reverse('v1:social', request=request, args=("facebook",))),
                ("Social Get Access Token", reverse('v1:get_access_token', request=request,
                                                    args=("facebook", "10aA_jhuiy"))),
                ("Feeds social links", reverse('v1:social_link-list', request=request)),
                ("Social Feed", reverse('v1:get_feeds', request=request, args=(1486972743,))),
                ("Social Content", reverse('v1:content-list', request=request, kwargs={'user_type': user_type})),
                ("Social Ignored Content", reverse('v1:ignored-content-list', request=request,
                                                   kwargs={'user_type': user_type})),
                ("Social Super Admin Content", reverse('v1:super-admin-content-list',
                                                       request=request, kwargs={'user_type': user_type})),
                ("Super Admin Content Unhide", reverse('v1:super-admin-content-unhide', request=request,
                                                       kwargs={'pk': 1})),
                ("Like Content", reverse('v1:content-like', request=request, kwargs={'user_type': user_type, 'pk': 1})),
                ("Unlike Content", reverse('v1:content-dislike', request=request,
                                           kwargs={'user_type': user_type, 'pk': 1})),
                ("Favorite Content", reverse('v1:content-favorite', request=request,
                                             kwargs={'user_type': user_type, 'pk': 1})),
                ("Remove Favorite Content", reverse('v1:content-remove-favorite', request=request,
                                                    kwargs={'user_type': user_type, 'pk': 1})),
            ])),
            ("Account APIs", OrderedDict([
                ("Account Link", reverse('v1:expert-accounts-list', request=request, kwargs={'user_type': user_type})),
            ])),
            ("Profile Status APIs", OrderedDict([
                ("Profile Status Check Link", reverse('v1:profile-status', request=request,
                                                      kwargs={'user_type': user_type})),
            ])),
            ("GetStream Feed APIs", OrderedDict([
                ("Expert Getstream Feed API", reverse('v1:expert-feed', request=request, kwargs={'expert_id': 1})),
                ("Tag Getstream Feed API", reverse('v1:tag-feed', request=request, kwargs={'tag_id': 1})),
                ("Expert Profile Getstream Feed API", reverse('v1:expert-profile-feed',
                                                              request=request, kwargs={'expert_profile_id': 1})),
                ("Super Admin Getstream Feed API", reverse('v1:superadmin-feed', request=request, )),
                ("Usre Global Getstream Feed API", reverse('v1:user-global-feed', request=request)),
                ("Expert Feeds Followed By User API", reverse('v1:me-following-experts', request=request, )),
                ("Tag Feeds Followed By User API", reverse('v1:me-following-tags', request=request)),
                ("User Aggregated Feeds", reverse('v1:user-aggregated-feeds', request=request)),
            ])),
            ("Calendar APIs", OrderedDict([
                ("Expert Slots", reverse('v1:slots-list', request=request, kwargs={'user_type': user_type})),
                ("Available Slots", reverse('v1:expert-slots', request=request,
                                            kwargs={'user_type': user_type, 'expert_id': 1})),
            ])),
            ("Rating & Reviews", OrderedDict([
                ("Expert Session Reviews", reverse('v1:expert-session-reviews', request=request,
                                                   kwargs={'user_type': user_type, 'pk': 1}))
            ])),
            ("Follow, Unfollow & Following Apis", OrderedDict([
                ("User Follow Expert APi", reverse('v1:follow-expert', request=request,
                                                   kwargs={'user_type': user_type, 'expert_id': 1})),
                ("User UnFollow Expert APi", reverse('v1:unfollow-expert', request=request,
                                                     kwargs={'user_type': user_type, 'expert_id': 1})),
                ("User Following, Expert List APi", reverse('v1:me-following', request=request,
                                                            kwargs={'user_type': user_type})),
                ("Expert Follower, User List APi", reverse('v1:me-followers', request=request,
                                                           kwargs={'user_type': user_type})),
                ("Tag Follow", reverse('v1:following-tags', request=request, kwargs={'user_type': user_type})),
            ])),
            ("SuperAdmin Promo Codes", OrderedDict([
                ("Promo Codes", reverse('v1:promo-code-list', request=request,))
            ])),
            ("Notification APIs", OrderedDict([
                ("Notification settings", reverse('v1:notification-settings', request=request,
                                                  kwargs={'user_type': user_type})),
            ])),
            ("Featured APIs", OrderedDict([
                ("Expert Featured List For User", reverse('v1:user-featured-experts', request=request,
                                                          kwargs={'user_type': user_type})),
                ("Expert Featured List For Super Admin", reverse('v1:super-featured-experts', request=request)),
            ])),
        ]))

    def get_view_name(self):
        """
        Return the view name, as used in OPTIONS responses and in the
        browsable API.
        """
        if not hasattr(self, 'kwargs'):
            return "Expert-User APIs"
        return "{} APIs".format(self.kwargs.get('user_type', 'user').capitalize())


class CMSApiRoot(APIView):
    def get(self, request):
        if not settings.ENABLE_API_ROOT:
            return Response(dict())

        return Response(OrderedDict([
            ("User Create", reverse('v1:superuser-list', request=request)),
            ("User Enable", reverse('v1:superuser-enable', request=request, kwargs={'pk': 1})),
            ("User Disable", reverse('v1:superuser-disable', request=request, kwargs={'pk': 1})),
        ]))
