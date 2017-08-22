ERROR_DUPLICATE_EMAIL = {"code": 1001, "message": "This email address is already tied to an existing account."}
ERROR_INVALID_PASSWORD = {"code": 1002, "message": "Your password must be at least 8 characters long and contain at least one number."}

ERROR_UNVERIFIED_EMAIL = {"code": 1011, "message": "Your email address has not been verified.  Please check your email for instructions."}
ERROR_INVALID_CREDENTIALS = {"code": 1012, "message": "Incorrect email or password provided.  Please check your information and try again."}
ERROR_REQUIRED_VALUE = {"code": 1013, "message": "Please provide a valid email address and password."}

ERROR_INVALID_CURRENT_PASSWORD = {"code": 1021, "message": "Incorrect password provided. Please re-enter your current password."}
ERROR_PASSWORD_REUSED = {"code": 1022, "message": "The password you entered is already in use. Please create a new password."}

ERROR_MAX_ATTEMPTS_PASSWORD_RESET = {"code": 1031, "message": "You have exceeded the number of password reset requests. Please wait 24 hours before submitting another request."}
ERROR_NO_EMAIL = {"code": 1032, "message": "This email address is currently not registered."}
ERROR_TOKEN_EXPIRED = {"code": 1033, "message": "Your password reset request has expired.  Please submit a new request."}

ERROR_VERIFICATION_LINK_EXPIRED = {"code": 1041, "message": "Your email verification request has expired. Please submit a new request."}
ERROR_INVALID_TOKEN = {"code": 1042, "message": "Your password reset request has expired.  Please submit a new request."}
ERROR_MAX_ATTEMPTS_EMAIL_VERIFY = {"code": 1043, "message": "You have exceeded the number of email verification requests. Please wait 24 hours before submitting another request."}
ERROR_EMAIL_ALREADY_VERIFIED = {"code": 1044, "message": "Email is already verified."}

ERROR_SOCIAL_LOGIN = {"code": 1051, "message": "Could not authenticate you, please try again."}
ERROR_RSS_FEED_INVALID = {"code": 1052, "message": "The provided URL is not a Valid RSS/FEED url."}
ERROR_CONTENT_HAS_BEEN_REMOVED = {"code": 1053, "message": "This content has been removed."}

ERROR_CONTENT_NOT_EXIST = {"code": 1054, "message": "This content doesn't exists."}
ERROR_CONTENT_ALREADY_PUBLISHED = {"code": 1055, "message": "This Content is already published."}
ERROR_CONTENT_ALREADY_IGNORED = {"code": 1056, "message": "This Content is already Ignored."}
ERROR_LINK_HAS_BEEN_REMOVED =  {"code": 1057, "message": "Selected links has been removed."}
ERROR_INVALID_PROVIDER = {"code": 1058, "message": "Invalid value for Feed type."}

ERROR_INVALID_ACCOUNT_NUMBER = {"code": 1061, "message": "Account Number should be numeric."}
ERROR_INVALID_ROUTING_NUMBER = {"code": 1062, "message": "Routing Number should be numeric."}
ERROR_INVALID_LENGTH_OF_ROUTING_NUMBER = {"code": 1063, "message": "Routing Number should be of 9 digit."}

ERROR_VERIFIED_PHONE = {"code": 1071, "message": "Phone number is already verified ."}
ERROR_OTP_NO_MATCH = {"code": 1072, "message": "The verification code does not match ."}
ERROR_MAX_OTP_REQUEST = {"code": 1073, "message": "OTP limit exceeded for today."}
ERROR_PHONE_INVALID = {"code": 1074, "message": "This number is not valid mobile number."}
ERROR_REGISTERED_NOT_VERIFIED = {"code": 1075, "message": "Phone number is already registered but not verified."}
ERROR_NO_MOBILE = {"code": 1076, "message": "The mobile number does not exist."}
ERROR_OTP_EXPIRED = {"code": 1077, "message": "This OTP has been expired. Please generate a new OTP."}

ERROR_VIDEO_SIZE_MAX = {"code": 1081, "message": "The maximum video size supported is 10 MB ."}
ERROR_IMG_SIZE_MAX = {"code": 1082, "message": "The maximum Image size supported is 2 MB ."}
ERROR_MEDIA_NOT_ALLOWED = {"code": 1083, "message": "The file type is not supported."}
ERROR_MEDIA_LIMIT_MAX = {"code": 1084, "message": "Maximum allowed medias has already been uploaded."}

ERROR_MEDIA_INVALID = {"code": 1091, "message": "One of the selected media is invalid."}
ERROR_TAG_MAX = {"code": 1092, "message": "You can select max 20 tags."}
ERROR_MAX_PROFILES = {"code": 1093, "message": "Maximum allowed profiles has already been created."}
ERROR_MAX_EXPERIENCE_CHARS = {"code": 1094, "message": "Max 1000 characters are allowed."}
ERROR_MAX_EDUCATIONAL_CHARS = {"code": 1095, "message": "Max 1000 characters are allowed."}
ERROR_DISPLAY_NAME_ALREADY_USED = {"code": 1096, "message": "Display name already taken."}

# Errors Related to the Appointment slots
ERROR_INVALID_END_TIME = {"code": 1101, "message": "Start time should be less than End Time"}
ERROR_INVALID_TIME = {"code": 1102, "message": "Start and End time, seconds value should "
                                               "not be used while creating the slots"}
ERROR_INVALID_INTERVAL_TIME = {"code": 1103, "message": "Interval between Start and End Time should be 20 mins"}
ERROR_INVALID_START_TIME_MINUTES = {"code": 1104, "message": "Start time minutes value should be multiple of 5"}
ERROR_INVALID_END_TIME_MINUTES = {"code": 1105, "message": "End time minutes value should be multiple of 5"}
ERROR_INVALID_TIMEZONE = {"code": 1106, "message": "You are requesting for Invalid timezone"}

ERROR_INVALID_DISCOUNT = {"code": 1111, "message": "You can not offer discount more than 100 %."}

# Error for follow and Unfollow
ERROR_INVALID_TAG_ID = {"code": 1121, 'message': "One of the selected tag ids is invalid."}
ERROR_MIN_REQUIRED_TAG = {"code": 1122, 'message': "At least one tag is required."}
ERROR_INVALID_NOTIFICATION_SETTING = {"code": 1131, "message": "Invalid Notification Settings."}
ERROR_INVALID_EXPERT_IDS = {"code": 1141, "message": "The Expert doesn't exist or already in featured category."}
ERROR_INVALID_EXPERT_PROFILE_FOR_REVIEW = {"code": 1142, 'message': "Complete the profile before "
                                                                    "submitting it for reviewing."}
ERROR_EXPERT_PROFILE_NOT_COMPLETE = {"code": 1143, "message": "The expert profile is not completed."}

# Global Errors
ERROR_REQUIRED = {"code": 4001, "message": "This field is required."}
ERROR_NULL = {"code": 4002, "message": "This field may not be null."}
ERROR_BLANK = {"code": 4003, "message": "This field may not be blank."}
ERROR_INVALID_EMAIL = {"code": 4004, "message": "Enter a valid email address."}
ERROR_INVALID_DATA_URI = {"code": 4005, "message": "Invalid data uri"}
