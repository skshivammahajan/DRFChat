import binascii
import io
import mimetypes
import os
import random
import string

import av
import phonenumbers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from phonenumbers.phonenumberutil import NumberParseException
from PIL import Image

from experchat.enumerations import ExpertProfileReviewStatus
from experchat.models.appointments import Calendar
from experchat.models.users import Expert, ExpertProfile
from experchat.utils import create_image_thumbnail, validate_data_uri
from feeds.models import SocialLink
from registration.models import VerificationToken
from sendsms.utils import SMSHelper
from users.models import ExpertAccount

User = get_user_model()


def upload_photo(data_uri_str):
    """
    Save image from data_uri along with thumbnails.

    Args:
        data_uri_str: Data URI. (https://en.wikipedia.org/wiki/Data_URI_scheme)
    Returns:
        Uploaded photo url.

    Raises:
        ValueError: Invalid Data URI.
    """

    data_uri = validate_data_uri(data_uri_str)

    filename = binascii.hexlify(os.urandom(20)).decode()
    file_ext = mimetypes.guess_extension(data_uri.mimetype)

    # Save image using django's default storage
    image_path = default_storage.save('{}{}'.format(filename, file_ext), ContentFile(data_uri.data))

    image_data = io.BytesIO(data_uri.data)

    # Save thumbnails
    for size in settings.PROFILE_PHOTO_THUMBNAIL_SIZES:
        image = Image.open(image_data)
        create_image_thumbnail(image, size[0], size[1], filename)

    return "{media_url}{image_path}".format(
        media_url=settings.MEDIA_URL,
        image_path=image_path
    )


def generate_mobile_verifciation_code():
    pl = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], settings.MAX_OTP_PHONE_LENGTH)
    verification_code = ''.join(str(p) for p in pl)
    return verification_code


def validate_phone(entered_phone):
    try:
        phone_obj = phonenumbers.parse(entered_phone)
    except(NumberParseException):
        return False
    if not phonenumbers.is_valid_number(phone_obj):
        return False
    phone_number_type = phonenumbers.number_type(phone_obj)   # Returns 0 for landline and 1 for Mobile
    if phone_number_type in [phonenumbers.PhoneNumberType.MOBILE, phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE]:
        return True
    else:
        return False


def check_status_expert_myinfo(user):
    return all([user.name, user.profile_photo, user.is_phone_number_verified, user.expert.display_name,
                user.toc_and_privacy_policy_accepted])


def check_status_user_myinfo(user):
    return all([user.name, user.profile_photo, user.is_phone_number_verified, user.user.display_name])


def check_status_expert_profiles(user):
    return ExpertProfile.objects.filter(expert__userbase=user).exclude(headline='').exists()


def check_status_expert_socialink(user):
    return SocialLink.objects.filter(account__expert__userbase=user, is_deleted=False).exists()


def check_expert_availibility_slot(user):
    return Calendar.objects.filter(expert__userbase=user).exists()


def check_expert_review_status(expert):
    """
    Return true, if expert doesn't have profile other than approved.
    """
    return not ExpertProfile.objects.filter(
        expert=expert,
    ).exclude(
        review_status=ExpertProfileReviewStatus.APPROVED_BY_SUPER_ADMIN.value,
    ).exists()


def check_expert_profile_completeness(user):
    if hasattr(user, 'user'):
        return check_status_user_myinfo(user)
    elif hasattr(user, 'expert'):
        return all([
            check_status_expert_myinfo(user),
            check_status_expert_profiles(user),
            check_status_expert_socialink(user),
            check_expert_availibility_slot(user),
        ])
    else:
        return all([user.name, user.profile_photo])


def generate_expert_uid(name):
    last_name = ''
    try:
        first_name, *middle, last_name = name.split()
    except ValueError:
        first_name = name

    uid_initial = first_name[0] + last_name[0] if last_name else first_name[0:2]
    characters = list(string.ascii_uppercase) + list(string.digits)
    code = random.sample(characters, settings.EXPERT_UID_SUFFIX_LEN)

    uid_random = ''.join(code)

    return uid_initial + uid_random


def save_expert_uid(name, instance):
    if not hasattr(instance, 'expert'):
        return True

    expert = instance.expert
    if expert.expert_uid:
        return True

    count = 1
    while count <= settings.MAX_RETRY_EXPERT_UID:
        unique_id = generate_expert_uid(name)
        expert.expert_uid = unique_id
        try:
            with transaction.atomic():
                expert.save()
            return True
        except IntegrityError:
            count += 1
    return False


def make_other_expert_account_inactive(expert_id):
    expert_accounts = ExpertAccount.objects.filter(expert=expert_id, is_active=True)
    if expert_accounts:
        for account in expert_accounts:
            account.is_active = False
            account.save()
        return True
    return True


def relating_expert_account(expert_id, account_id):
    expert = Expert.objects.get(userbase=expert_id)
    expert.account_id = account_id.id
    expert.save()
    return True


def create_video_thumbnail(video, filename):
    container = av.open(video)
    try:
        video = [s for s in container.streams if s.type == 'video'][0]
    except IndexError:
        # return if no video stream is found.
        return None

    count = 0
    for packet in container.demux(video):
        for frame in packet.decode():
            count += 1
        if count >= settings.VIDEO_LAST_FRAME_FOR_THUMBNAIL:
            break

    for size in getattr(settings, 'VIDEO_THUMBNAIL_SIZES', [(600, 400)]):
        create_image_thumbnail(frame.to_image(), size[0], size[1], filename)


def send_verification_phone_otp(user):
    """
    Sends email to verify email on signup or requesting to send verification email again.

    Args:
        user: User base instance.
    Returns:
        Unique verification token to verify email for testing automation.
    """
    verification_token_obj = VerificationToken.objects.filter(
        user=user,
        purpose=VerificationToken.PHONE_VERIFICATION,
        created_timestamp__gt=(timezone.now()-timezone.timedelta(minutes=settings.PHONE_VERIFICATION_TOKEN_EXPIRY)),
        expired_at__isnull=True
    ).first()

    if verification_token_obj is None:
        verification_token = generate_mobile_verifciation_code()
        VerificationToken.objects.create(
            user=user,
            token=verification_token,
            purpose=VerificationToken.PHONE_VERIFICATION
        )
    else:
        verification_token_obj.notify_count += 1
        verification_token_obj.token = generate_mobile_verifciation_code()
        verification_token_obj.save()
        verification_token = verification_token_obj.token

    return verification_token


def send_sms_to_phone(user_country_code, user_phone, user):
    to = '+' + str(user_country_code) + user_phone
    passcode = send_verification_phone_otp(user)
    body = settings.PHONE_VERIFICATION_TEXT.format(otp_code=passcode)
    SMSHelper().send_sms(to, body)
    return passcode
