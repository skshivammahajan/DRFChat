from experchat.choices import ChoiceEnum


class CallStatus(int, ChoiceEnum):
    INITIATED = 1
    ACCEPTED = 2
    DECLINED = 3
    COMPLETED = 4
    DELAYED = 5
    SCHEDULED = 6


class DeviceStatus(int, ChoiceEnum):
    ACTIVE = 1
    INACTIVE = 2


class RatingValue(int, ChoiceEnum):
    """
    Choices for Provider
    """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class ExpertNotificationSettingCodes(str, ChoiceEnum):
    REVIEW_SESSION = 'review-session'
    DAILY_SUMMARY_REPORT = 'daily-summary-report'


class TagTypes(str, ChoiceEnum):
    PARENT = 'parent'
    CHILD = 'child'
    SYNONYM = 'synonym'


class ExpertProfileReviewStatus(int, ChoiceEnum):
    """
    Choices for Expert Profile Status for Reviewing by SuperAdmin .
    """
    NOT_SUBMITTED_FOR_REVIEW = 1
    SUBMITTED_FOR_REVIEW = 2
    APPROVED_BY_SUPER_ADMIN = 3
    REJECTED_BY_SUPER_ADMIN = 4
