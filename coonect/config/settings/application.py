# Session duration to consider session in session count stats for expert
SESSION_MIN_DURATION_FOR_STATS = 10  # in seconds

PUBNUB_PUSH_TIMEOUT = 30  # seconds

TOKBOX_TOKEN_EXPIRE_TIME = 30*60  # in seconds (30 minutes)

# Time to extend current session schedule time in minutes
SESSION_EXTENSION_TIME = 10

# Price for session extension
SESSION_EXTENSION_PRICE = 15  # (in dollars)

# Duration from current time to consider scheduled session in future
SESSION_GRACE_DURATION = 5 * 60  # (in seconds)

SESSION_MIN_DURATION_FOR_REVENUE = 5 * 60  # in seconds

# Session Cancellation settings
SESSION_CANCELLATION_PERCENTAGE_AMOUNT = 25
NO_CANCELLATION_CHARGES_POST_SCHEDULE_DURATION = 2  # in hours
NO_CANCELLATION_CHARGES_PRIOR_APPOINTMENT_DURATION = 24  # in hours

# No of days for which notifications will be returned
NOTIFICATION_DAYS = 10
