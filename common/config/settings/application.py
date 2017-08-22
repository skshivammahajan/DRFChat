# Email Request Settings
from celery.schedules import crontab

RESEND_VERIFY_EMAIL_LIMIT = 5  # No of request user can make for email verification .
RESET_PASSWORD_EMAIL_LIMIT = 5  # No of request user can make for password reset .

# Verification token expiry
# NOTE: Always set below three values in minutes
EMAIL_VERIFICATION_TOKEN_EXPIRY = 1*24*60  # (in minutes) Number of days to expire email verification token
PHONE_VERIFICATION_TOKEN_EXPIRY = 10  # (in minutes) Number of minutes to expire otp (phone verification token)
PASSWORD_RESET_TOKEN_EXPIRY = 1*24*60  # (in minutes) Number of days to expire password reset token

# Profile Settings
NUM_PROFILE_USER_ALLOWED = 1 # No. of profiles allowed for an user .

# Media Settings
MEDIA_TYPE_IMAGE = 'image'
MEDIA_TYPE_VIDEO = 'video'
ALLOWED_MEDIA_TYPES = [MEDIA_TYPE_IMAGE, MEDIA_TYPE_VIDEO]

MAX_IMG_SIZE = 2 * 1024 * 1024 # image size (in bytes 2MB)
MAX_VID_SIZE = 10 * 1024 * 1024 # video size (in bytes 10MB)
ALLOWED_MEDIA_RECORD = 10 # No of media files (images/videos) allowed to be uploaded by each user .

# FEEDS configurations

# Feeds providers
FACEBOOK_FEED_PROVIDER = ['FB', 'FACEBOOK']
INSTAGRAM_FEED_PROVIDER = ['INSTAGRAM']
YOUTUBE_FEED_PROVIDER = ['YOUTUBE', 'GOOGLE']
ALL_FEED_PROVIDERS = ['FB', 'FACEBOOK', 'INSTAGRAM', 'YOUTUBE', 'GOOGLE']
FACEBOOK_REDIRECT_URL = "http://web.qa.experchat.com/redirects/facebook/"
INSTAGRAM_REDIRECT_URL = "http://web.qa.experchat.com/redirects/instagram/"
YOUTUBE_REDIRECT_URL = "http://web.qa.experchat.com/redirects/youtube/"

FEEDS_OFFSET_LIMIT = 10
FEED_CACHE_KEY_PREFIX = 'FEEDS'
SOCIAL_KEY_MAPPING = {
    'FACEBOOK': 'fb_',
    'INSTAGRAM': 'in_',
    'YOUTUBE': 'yt_',
    'GOOGLE': 'yt_',
    'RSS': 'rs_',
    'EXPERT_CHAT': 'su_'
}
USER_FEED_TYPE = 1

MAX_TAGS_COUNT = 20
MAX_EXPERIENCE_CHAR = 1000
MAX_EDU_BACK_CHAR = 1000

# PHONE OTP LENGTH sent to user mobile
MAX_OTP_PHONE_LENGTH = 6
RESET_PHONE_OTP_LIMIT = 5
PHONE_VERIFICATION_TEXT = "Use OTP {otp_code} to verify your mobile number on ExperChat App."

# Stream conf
STREAM_FEEDS_EXPERTS = 'expert'
STREAM_FEEDS_EXPERT_PROFILE = 'expertprofile'
STREAM_FEEDS_TAG = 'tag'
STREAM_FEEDS_USER = 'user'
STREAM_VERBS_POST = 'post'
STREAM_READ_LIMIT = 50
STREAM_STATIC_GLOBAL_FEED = 'global'
STREAM_STATIC_SUPERADMIN_FEED = 'superadmin'
USER_AGGREGATED_TIMELINE_FEED = 'user_aggregated'

# Length of Suffix to be added in Expert UID
EXPERT_UID_SUFFIX_LEN = 3

# No. of times system can  handle the Integrity error while generating Expert UID
MAX_RETRY_EXPERT_UID = 20

# Video Thumbnail
VIDEO_LAST_FRAME_FOR_THUMBNAIL = 100
VIDEO_THUMBNAIL_SIZES = [
    (600, 400),
]

# Appointment Related Settings, once you are modifying this, modidfy the error message as well
APPOINTMENT_MINUTES_INTERVAL = 5
APPOINTMENT_START_END_TIME_INTERVAL = 20


TMP_MEDIA_CLEANUP_TASK_SCHEDULE = crontab(minute=0, hour=0)  # Execute daily at midnight.
CLEAN_TMP_MEDIA_OLDER_THAN = 24*60  # (in minutes) Remove unused medias created before.

# Minimum number of tags need to be followed by User
MIN_REQUIRED_TAG = 1

# SNS LOGO URLS
AWS_FB_LOGO = "https://experchat.s3.amazonaws.com/logo/facebook.png"
AWS_INSTA_LOGO = "https://experchat.s3.amazonaws.com/logo/instagra-email.png"
AWS_EXPERCHAT_LOGO = "https://experchat.s3.amazonaws.com/logo/Logo-diaomond.png"
AWS_TWIT_LOGO = "https://experchat.s3.amazonaws.com/logo/twitter.png"

# Email Address where expert profile are to be sent for approval.
EMAIL_FOR_EXPERT_PROFILE_SEND_APPROVAL = 'marketing@experchat.com'

# Display Name for Super Admins
EC_ADMIN_DISPLAY_NAME = 'ExperChat staff'

# Calender related settings
MAX_AVAILABLE_SLOTS_LIMIT = 10
NEXT_SLOTS_LIMITS = 14

# Templates Title for T&C and Privacy Policy
TERMS_AND_CONDITION_TEMPLATE_TITLE = "Terms of Use"
PRIVACY_POLICY_TEMPLATE_TITLE = "Privacy Policy"
