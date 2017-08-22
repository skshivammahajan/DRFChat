from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Case, Count, IntegerField, Q, When
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone
from PIL import Image
from rest_framework import generics, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from experchat.enumerations import ExpertProfileReviewStatus
from experchat.messages import get_message
from experchat.models.appointments import Calendar
from experchat.models.domains import Tag
from experchat.models.notification_setting import ExpertNotificationSettings
from experchat.models.promocodes import PromoCode
from experchat.models.ratings import SessionRating
from experchat.models.users import Expert, ExpertProfile, FollowExpert, User, UserMedia
from experchat.permissions import IsExpertPermission, IsOwnerOrReadOnly, IsSuperUser, IsUserPermission
from experchat.serializers import (
    CalendarSerializer, EmptySerializer, ExpertProfileDetailSerializer, ExpertProfileListSerializer,
    ExpertProfileSerializer, SessionRatingSerializer, TagSerializer, UserSerializer
)
from experchat.utils import (
    create_image_thumbnail, custom_send_mail, filter_slots, get_booked_and_available_slots, split_and_update_price
)
from experchat.views import ExperChatAPIView
from feeds.models import SocialLink
from feeds.serializers import SocialLinkSerializer, SocialLinkUpdateSerializer
from streamfeeds.utils import StreamHelper
from users.models import ExpertAccount, FollowTags
from users.serializers import (
    ExpertAccountSerializer, ExpertBasicInfoSerializer, ExpertNotificationSettingsSerializer, FeaturedExpertSerializer,
    MediaSerializer, PhoneCodeSendSerializer, PhoneVerifySerializer, PhotoUploadSerializer, PromoCodeSerializer,
    ResendPhoneCodeSendSerializer, UserBasicInfoSerializer
)
from users.utils import (
    check_expert_availibility_slot, check_expert_profile_completeness, check_status_expert_myinfo,
    check_status_expert_profiles, check_status_expert_socialink, create_video_thumbnail,
    make_other_expert_account_inactive, relating_expert_account, send_sms_to_phone, upload_photo
)

UserBase = get_user_model()


class BasicInfoView(generics.RetrieveUpdateAPIView):
    """
    Basic information of User/Expert.
    """
    queryset = UserBase.objects.all()
    serializer_class = UserBasicInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.request.user.id)

    def get_serializer_class(self):
        if self.kwargs.get('user_type') == 'expert':
            return ExpertBasicInfoSerializer
        return super(BasicInfoView, self).get_serializer_class()


class PhotoUploadView(ExperChatAPIView):
    """
    Profile Picture Upload by User .
    """
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoUploadSerializer
    throttle_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_uri_str = serializer.validated_data['image']

        try:
            image_url = upload_photo(data_uri_str)
        except ValueError:
            return Response({"detail": get_message('ERROR_INVALID_DATA_URI')}, status=status.HTTP_400_BAD_REQUEST)

        image_url = request.build_absolute_uri(image_url)
        request.user.profile_photo = image_url
        request.user.save()

        return Response({"image_url": image_url})


class ExpertProfileView(viewsets.ModelViewSet):
    """
    Manage Expert Profiles.

    Expert Profile Approval Status (`review_status`) options:

        NOT_SUBMITTED_FOR_REVIEW = 1
        SUBMITTED_FOR_REVIEW = 2
        APPROVED_BY_SUPER_ADMIN = 3
        REJECTED_BY_SUPER_ADMIN = 4
    """
    queryset = ExpertProfile.objects.all().select_related('expert__userbase')
    serializer_class = ExpertProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(expert=self.request.user.expert)

    def get_queryset(self):
        queryset = super(ExpertProfileView, self).get_queryset()
        if hasattr(self.request.user, 'expert'):
            queryset = queryset.filter(expert=self.request.user.expert)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ExpertProfileListSerializer
        if self.action == 'retrieve':
            return ExpertProfileDetailSerializer

        return super(ExpertProfileView, self).get_serializer_class()

    # @detail_route(methods=['PUT'], serializer_class=SocialLinkUpdateSerializer)
    def update_social_links(self, request, user_type, pk=None):
        serializer = SocialLinkUpdateSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        # set B of social links to update for Expert profile
        social_link_ids = serializer.validated_data['social_link_ids']
        obj = self.get_object()  # Expert Profile
        # set A of existing social links linked to Expert Profile
        existing_social_links = SocialLink.objects.filter(expert_profiles=obj.id).values_list('id', flat=True)

        social_link_ids_add = list(set(social_link_ids) - set(existing_social_links))   # B-A
        social_link_ids_remove = list(set(existing_social_links) - set(social_link_ids))  # A-B

        obj.social_links.remove(*social_link_ids_remove)  # Remove A-B from database
        obj.social_links.add(*social_link_ids_add)  # Add B-A in database

        return Response(status=status.HTTP_200_OK, data={
            'social_link_ids': social_link_ids_add
        })

    @detail_route(methods=['put'], permission_classes=(IsExpertPermission,), serializer_class=EmptySerializer)
    def submit_for_review(self, request, user_type=None, pk=None, ):
        obj = self.get_object()
        # Check whether expert Profile is completed or not
        if not check_expert_profile_completeness(request.user):
            return Response(
                {
                    "errors": {
                        api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_INVALID_EXPERT_PROFILE_FOR_REVIEW')
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check whether the profile is already submitted for Review .
        if obj.review_status == ExpertProfileReviewStatus.NOT_SUBMITTED_FOR_REVIEW.value or \
                ExpertProfileReviewStatus.REJECTED_BY_SUPER_ADMIN.value:
            obj.review_status = ExpertProfileReviewStatus.SUBMITTED_FOR_REVIEW.value
            obj.profile_submitted_timestamp = timezone.now()
            obj.save()

            # Emailing the Expert Profile Detail to SuperAdmin
            mail_context = {
                'expert_name': obj.expert.display_name,
                'headline': obj.headline,
                'summary': obj.summary,
            }
            custom_send_mail(
                'expert/profile_review_email_subject.txt',
                'expert/profile_review_email.txt',
                mail_context,
                settings.EMAIL_FOR_EXPERT_PROFILE_SEND_APPROVAL,
                html_email_template_name='expert/profile_review_email.html',
            )
        return Response({"review_status": obj.review_status})

    @detail_route(methods=['put'], permission_classes=(IsSuperUser,), serializer_class=EmptySerializer)
    def approve_profile(self, request, pk=None, user_type=None):
        obj = self.get_object()
        if obj.review_status == ExpertProfileReviewStatus.SUBMITTED_FOR_REVIEW.value:
            obj.review_status = ExpertProfileReviewStatus.APPROVED_BY_SUPER_ADMIN.value
            obj.save()
            mail_context = {
                'expert_name': obj.expert.display_name,
                'headline': obj.headline,
                'summary': obj.summary,
            }
            custom_send_mail(
                'expert/review_profile_approval_status_email_subject.txt',
                'expert/review_profile_accept_email.txt',
                mail_context,
                self.request.user.email,
                html_email_template_name='expert/review_profile_accept_email.html',
            )
        return Response({"review_status": obj.review_status})

    @detail_route(methods=['put'], permission_classes=(IsSuperUser,), serializer_class=EmptySerializer)
    def reject_profile(self, request, pk=None, user_type=None):
        obj = self.get_object()
        if obj.review_status == ExpertProfileReviewStatus.SUBMITTED_FOR_REVIEW.value:
            obj.review_status = ExpertProfileReviewStatus.REJECTED_BY_SUPER_ADMIN.value
            obj.save()
            mail_context = {
                'expert_name': obj.expert.display_name,
                'headline': obj.headline,
                'summary': obj.summary,
            }
            custom_send_mail(
                'expert/review_profile_approval_status_email_subject.txt',
                'expert/review_profile_reject_email.txt',
                mail_context,
                self.request.user.email,
                html_email_template_name='expert/review_profile_reject_email.html',
            )
        return Response({"review_status": obj.review_status})


class ExpertProfileSocialLinksListView(generics.ListAPIView):
    """
    All the social profiles associated with user accounts .
    """
    queryset = SocialLink.objects.filter(is_deleted=False)
    serializer_class = SocialLinkSerializer
    permission_classes = (IsExpertPermission,)

    def get_queryset(self):
        queryset = super(ExpertProfileSocialLinksListView, self).get_queryset()

        expert_profile = ExpertProfile.objects.filter(pk=self.kwargs['pk'])
        queryset = queryset.filter(expert_profiles=expert_profile)

        return queryset


class UserMediaViewSet(viewsets.ModelViewSet):
    """
    ViewSet to allow user to manage medias.
    """
    serializer_class = MediaSerializer
    queryset = UserMedia.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(UserMediaViewSet, self).get_queryset()

        queryset = queryset.filter(owner=self.request.user)

        return queryset

    def perform_create(self, serializer):
        media = serializer.validated_data["media"]
        content_type = media.content_type.split('/')[0]
        instance = serializer.save(owner=self.request.user, media_type=content_type)
        filename = instance.media.name.rsplit('.', 1)[0]

        if content_type == settings.MEDIA_TYPE_VIDEO:
            create_video_thumbnail(instance.media, filename)

        if content_type == settings.MEDIA_TYPE_IMAGE:
            for size in settings.PROFILE_PHOTO_THUMBNAIL_SIZES:
                image = Image.open(instance.media)
                create_image_thumbnail(image, size[0], size[1], filename)

    def perform_destroy(self, instance):
        instance.media.delete()  # Remove media from S3
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()

        if 'media' in serializer.validated_data:
            instance.media.delete()  # Remove media from S3
            content = serializer.validated_data["media"]
            content_type = content.content_type.split('/')[0]
            instance = serializer.save(media_type=content_type)
        else:
            instance = serializer.save()
        return instance


class PhoneCodeSendView(GenericAPIView):
    """
    Viewset to send verification code to  user phone .
    """
    queryset = UserBase.objects.all()
    serializer_class = PhoneCodeSendSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_country_code = serializer.validated_data["country_code"]
        user_phone = serializer.validated_data["mobile"]
        user = self.request.user

        passcode = send_sms_to_phone(user_country_code, user_phone, user)

        user.country_code = user_country_code
        user.phone_number = user_phone
        user.is_phone_number_verified = False
        user.save()

        response = {'results': get_message('OK_PHONE_OTP_RESEND')}

        if getattr(settings, 'TEST_MODE', False):
            response['results'].update(
                verification_code=passcode
            )
        return Response(response)


class PhoneVerifyView(GenericAPIView):
    """
    Verify User's Phone Number.
    """
    serializer_class = PhoneVerifySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_token_obj = serializer.validated_data['verification_token_obj']
        verification_token_obj.perform_verification()

        return Response(
            {"detail": get_message('OK_PHONE_VERIFIED')}
        )


class ResendPhoneCodeSendView(GenericAPIView):
    """
    Resend verification code to user's mobile .
    """
    queryset = UserBase.objects.all()
    serializer_class = ResendPhoneCodeSendSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_country_code = serializer.validated_data['country_code']
        user_phone = serializer.validated_data['mobile']
        user = self.request.user

        passcode = send_sms_to_phone(user_country_code, user_phone, user)

        response = {'results': get_message('OK_PHONE_OTP_RESEND')}

        if getattr(settings, 'TEST_MODE', False):
            response['results'].update(
                verification_code=passcode
            )
        return Response(response)


class ProfileStatusView(ExperChatAPIView):
    """
    Profile Status check .
    """
    permission_classes = (IsAuthenticated, IsExpertPermission)

    def get(self, request, *args, **kwargs):
        response = {
            'is_myinfo_complete': check_status_expert_myinfo(request.user),
            'is_expertprofiles_exist': check_status_expert_profiles(request.user),
            'is_socialink_exist': check_status_expert_socialink(request.user),
            'has_availibility_slot': check_expert_availibility_slot(request.user),
        }
        return Response(response)


class ExpertAccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet to allow user to manage account information.
    """
    serializer_class = ExpertAccountSerializer
    queryset = ExpertAccount.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, IsExpertPermission)
    http_method_names = ('get', 'post')

    def get_queryset(self):
        queryset = super(ExpertAccountViewSet, self).get_queryset()
        queryset = queryset.filter(expert=self.request.user)
        return queryset

    def perform_create(self, serializer):
        accounts = make_other_expert_account_inactive(self.request.user.id)
        if accounts:
            last_account = ExpertAccount.objects.filter(
                expert=self.request.user
            ).order_by('-modified_timestamp').first()
            kwargs = dict()
            if last_account is not None:
                kwargs = dict(
                    account_name=serializer.validated_data.get('account_name', last_account.account_name),
                    account_number=serializer.validated_data.get('account_number', last_account.account_number),
                    routing_number=serializer.validated_data.get('routing_number', last_account.routing_number),
                )
            account_id = serializer.save(
                expert=self.request.user, **kwargs
            )
            if account_id:
                relating_expert_account(self.request.user.id, account_id)
            return account_id

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(partial=True, *args, **kwargs)


class CalendarViewSet(viewsets.ModelViewSet):
    """
    ViewSet to allow user to manage Calendar information(book appointment etc)
    """
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()
    permission_classes = (IsExpertPermission, )

    def get_queryset(self):
        queryset = super(CalendarViewSet, self).get_queryset()
        queryset = queryset.filter(expert=self.request.user.expert)
        return queryset.order_by('start_time')

    def perform_create(self, serializer):
        serializer.save(expert=self.request.user.expert)


class ExpertAppointmentsView(ExperChatAPIView):
    """
    View for Expert
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_type=None, expert_id=None, format=None):
        time_zone = request.query_params.get('timezone')
        available_slots, booked_slots = get_booked_and_available_slots(expert_id)
        filtered_slots = filter_slots(available_slots, booked_slots)
        final_slots = split_and_update_price(filtered_slots, time_zone)
        final_data = {'metadata': {'expert_id': expert_id},
                      'results': final_slots}

        return Response(final_data)


class TermsAndPolicyView(APIView):
    """
    View to returns terms and condition and privacy policy from html template in string format
    """
    def get(self, request, *args, **kwargs):
        # Make the condition type to get the exact template name
        if kwargs['condition_type'] == 'toc':
            condition_type = 'terms_and_condition'
        else:
            condition_type = kwargs['condition_type']
        template_name = "{user_type}/{condition_type}.html".format(
            user_type=kwargs['user_type'],
            condition_type=condition_type
        )
        template_title = getattr(settings, '%s_TEMPLATE_TITLE' % condition_type.upper())
        return Response({'body': loader.render_to_string(template_name), 'title': template_title})


class TermsAndPolicyAcceptView(APIView):
    """
    View for accepting the terms and condition
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not self.request.user.toc_and_privacy_policy_accepted:
            self.request.user.toc_and_privacy_policy_accepted = True
            self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TermsAndPolicySendMailView(APIView):
    """
    View to send terms and contion or privacy policy to user/expert
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Make the condition type to get the exact template name
        if kwargs['condition_type'] == 'toc':
            condition_type = 'terms_and_condition'
        else:
            condition_type = kwargs['condition_type']
        template_name = "{user_type}/{condition_type}.txt".format(
            user_type=self.kwargs['user_type'],
            condition_type=condition_type
        )
        html_template_name = "{user_type}/{condition_type}.html".format(
            user_type=self.kwargs['user_type'],
            condition_type=condition_type
        )
        email_subject_template_name = '{condition_type}_email_subject.txt'.format(
            condition_type=condition_type
        )
        custom_send_mail(
            email_subject_template_name,
            template_name,
            {},
            request.user.email,
            html_email_template_name=html_template_name
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionReviewView(generics.ListAPIView):
    queryset = SessionRating.objects.all().order_by('-created_timestamp')
    serializer_class = SessionRatingSerializer

    def get_queryset(self):
        queryset = super(SessionReviewView, self).get_queryset()
        queryset = queryset.filter(session__expert=self.kwargs['pk'])
        return queryset


class FollowExpertView(APIView):
    """
    View for Following the Expert by user
    """
    permission_classes = (IsUserPermission,)

    def post(self, request, expert_id, *args, **kwargs):
        expert = get_object_or_404(Expert, pk=expert_id)
        try:
            FollowExpert.objects.create(user=request.user.user, expert=expert)
            # follow expert in streamfeed
            StreamHelper().follow_experts(expert.id, request.user.user)
        except IntegrityError:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnFollowExpertView(APIView):
    """
    View for UnFollowing the Expert by user
    """
    permission_classes = (IsUserPermission,)

    def post(self, request, expert_id, *args, **kwargs):
        expert = get_object_or_404(Expert, pk=expert_id)
        instance_deleted = FollowExpert.objects.filter(user__userbase=request.user, expert=expert).delete()
        if instance_deleted[0] > 0:
            # unfollow the expert from streamfeeds
            StreamHelper().unfollow_expert(expert.id, request.user.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowingExpertListView(generics.ListAPIView):
    """
    View for Listing the Expert which are followed by User
    """
    queryset = ExpertProfile.objects.all()
    serializer_class = ExpertProfileListSerializer
    permission_classes = (IsUserPermission, )

    def get_queryset(self):
        queryset = super(UserFollowingExpertListView, self).get_queryset()
        queryset = queryset.filter(expert__followers__user__userbase=self.request.user.id).distinct()
        queryset = queryset.annotate(
            content_count=Count(
                Case(
                    When(
                        expert__userbase__contents__is_deleted=False,
                        expert__userbase__contents__created_timestamp__gte=timezone.now() - timedelta(hours=24),
                        then=1
                    ),
                    output_field=IntegerField(),
                ),
            )
        )
        queryset = queryset.order_by('-content_count')
        return queryset


class ExpertFollowedByListView(generics.ListAPIView):
    """
    View for Listing the Expert which are followed by User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsExpertPermission,)

    def get_queryset(self):
        queryset = super(ExpertFollowedByListView, self).get_queryset()

        queryset = queryset.filter(following__expert__userbase=self.request.user).distinct()

        return queryset


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = (IsSuperUser,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status', 'coupon_code', 'is_deleted')

    def get_queryset(self):
        queryset = super(PromoCodeViewSet, self).get_queryset()
        if 'is_deleted' not in self.request.query_params:
            queryset = queryset.filter(is_deleted=False)
        if 'allowed_experts' in self.request.query_params:
            queryset = queryset.filter(
                Q(allowed_experts__isnull=True) | Q(allowed_experts=self.request.query_params.get('allowed_experts')))

        if 'allowed_users' in self.request.query_params:
            queryset = queryset.filter(
                Q(allowed_users__isnull=True) | Q(allowed_users=self.request.query_params.get('allowed_users')))

        return queryset


class FollowTagsView(APIView):
    """
    View for Tags being followed  by user .
    """
    queryset = Tag.objects.order_by('id').all()
    tag_serializer_class = TagSerializer
    permission_classes = (IsUserPermission,)

    def put(self, request, *args, **kwargs):

        # New Tag ids passed as the request to be followed by the user
        new_tag_ids = request.data
        stream_helper = StreamHelper()
        # User needs to follow at least One Tag
        if len(new_tag_ids) < settings.MIN_REQUIRED_TAG:
            return Response(
                {
                    "errors": {
                        api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_MIN_REQUIRED_TAG')
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Checking for invalid ids
        valid_tag_ids = Tag.objects.filter(id__in=new_tag_ids).count()
        if len(new_tag_ids) != valid_tag_ids:
            return Response(
                {
                    "errors": {
                        api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_INVALID_TAG_ID')
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tag ids already being followed by the user
        existing_tag_ids = FollowTags.objects.filter(user_id=request.user.user).values_list('tag_id', flat=True)

        # Remove Tags which user doesn't want to follow
        tags_ids_to_be_removed = set(existing_tag_ids) - set(new_tag_ids)
        # if any tag ids needs to be removed then we need to unfollow that tags from getstream
        FollowTags.objects.filter(tag_id__in=tags_ids_to_be_removed).delete()
        stream_helper.unfollow_tags(tags_ids_to_be_removed, request.user.user)

        # New Tags user wants to follow
        tags_ids_to_be_added = set(new_tag_ids) - set(existing_tag_ids)
        # Creating the new tag_ids to follow
        new_objs = [FollowTags(user=request.user.user, tag=Tag(tag_id)) for tag_id in tags_ids_to_be_added]
        FollowTags.objects.bulk_create(new_objs)
        stream_helper.follow_tags(new_objs, request.user.user)

        queryset = self.queryset.filter(id__in=new_tag_ids)
        serializer = self.get_tag_serializer(request, queryset)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(followers__user__userbase=request.user).distinct()
        serializer = self.get_tag_serializer(request, queryset)
        return Response(serializer.data)

    def get_tag_serializer(self, request, queryset):
        return self.tag_serializer_class(queryset, many=True, context={'request': request})


class ExpertNotificationSettingsView(APIView):
    permission_classes = (IsExpertPermission,)
    serializer_class = ExpertNotificationSettingsSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Settings which are already set for the user
        settings_already_existed = ExpertNotificationSettings.objects.filter(
            userbase=self.request.user).values_list('code', flat=True)
        # Settings for which the user want to update status
        settings_to_be_updated = set.intersection(set(serializer.validated_data.keys()), set(settings_already_existed))
        # New settings to be set for the user
        settings_to_be_created = set(serializer.validated_data.keys()) - set(settings_already_existed)

        # Updating the status of existing settings
        for i in settings_to_be_updated:
            ExpertNotificationSettings.objects.filter(code=i).update(status=request.data[i])

        # Creating the new settings
        objs_create = (ExpertNotificationSettings(
            userbase=self.request.user, code=i, status=request.data[i]) for i in settings_to_be_created)
        ExpertNotificationSettings.objects.bulk_create(objs_create)

        settings = dict(
            ExpertNotificationSettings.objects.filter(userbase=self.request.user).values_list('code', 'status')
        )
        serializer = ExpertNotificationSettingsSerializer(settings)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        settings = dict(
            ExpertNotificationSettings.objects.filter(userbase=self.request.user).values_list('code', 'status')
        )
        serializer = ExpertNotificationSettingsSerializer(settings)
        return Response(serializer.data)


class SuperAdminFeaturedExpertsView(APIView):
    """
    API for SuperAdmin to list, add and remove Expert in Featured Category.
    """
    queryset = ExpertProfile.objects.all()
    expert_serializer_class = FeaturedExpertSerializer
    permission_classes = (IsSuperUser, )

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_featured=True)
        serializer = self.expert_serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwars):
        # Passing list of expert ids in request
        expert_ids = request.data
        expert_profiles = ExpertProfile.objects.filter(expert_id__in=expert_ids, is_featured=False)
        # Check any invalid expert id or already exist in featured list
        if len(expert_ids) != len(expert_profiles):
            return Response(
                {
                    "errors": {
                        api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_INVALID_EXPERT_IDS')
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        for profiles in expert_profiles:
            if not check_expert_profile_completeness(profiles.expert.userbase):
                return Response(
                    {
                        "errors": {
                            api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_EXPERT_PROFILE_NOT_COMPLETE')
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        expert_profiles.update(is_featured=True)
        queryset = self.queryset.filter(expert__in=expert_ids)
        serializer = self.expert_serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        # Passing list of expert ids in request
        expert_ids = request.data
        expert_profiles = ExpertProfile.objects.filter(expert_id__in=expert_ids, is_featured=True)
        # Check any invalid expert id or doesn't exist in featured list
        if len(expert_ids) != len(expert_profiles):
            return Response(
                {
                    "errors": {
                        api_settings.NON_FIELD_ERRORS_KEY: get_message('ERROR_INVALID_EXPERT_IDS')
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        expert_profiles.update(is_featured=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeaturedExpertsListView(ExperChatAPIView):
    """
    API for listing all the featured experts visible to user.
    """
    queryset = ExpertProfile.objects.all()
    serializer_class = FeaturedExpertSerializer
    # permission_classes = (IsUserPermission,)

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_featured=True)
        serializer = self.serializer_class(queryset, many=True)
        # Sort experts  with highest number of content post and avg_rating
        sorted_data = sorted(serializer.data,
                             key=lambda data: (data['content_count'], data['expert']['avg_rating']), reverse=True)
        return Response(sorted_data)


class ExpertProfileList(generics.ListAPIView):
    """
    View for Listing the Expert Profiles which ares submitted for review.

    Expert Profile Approval Status (`review_status`) options:

        PENDING = 2
        APPROVE = 3
    """
    queryset = ExpertProfile.objects.all()
    serializer_class = ExpertProfileListSerializer
    permission_classes = (IsSuperUser,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('review_status',)

    def get_queryset(self):
        queryset = super(ExpertProfileList, self).get_queryset()
        queryset = queryset.filter(
            review_status__in=[ExpertProfileReviewStatus.SUBMITTED_FOR_REVIEW.value,
                               ExpertProfileReviewStatus.APPROVED_BY_SUPER_ADMIN.value]).order_by('-modified_timestamp')
        return queryset


class ExpertProfileDetail(APIView):
    """
    API for viewing the Expert Profile Detail.
    """
    permission_classes = (IsSuperUser,)

    def get(self, request, *args, **kwargs):
        expert_profile = get_object_or_404(
            ExpertProfile, expert=self.kwargs['pk'],
            review_status__in=[ExpertProfileReviewStatus.SUBMITTED_FOR_REVIEW.value,
                               ExpertProfileReviewStatus.APPROVED_BY_SUPER_ADMIN.value])
        availability_slots = Calendar.objects.filter(expert=expert_profile.expert)
        social_links = SocialLink.objects.filter(account__expert=expert_profile.expert)
        response = {
            "basic_info": ExpertBasicInfoSerializer(expert_profile.expert.userbase).data,
            "profiles": ExpertProfileSerializer(expert_profile).data,
            "slots": CalendarSerializer(availability_slots, many=True).data,
            "social_links": SocialLinkSerializer(social_links, many=True).data,
        }
        return Response(response)
