from enum import Enum


# class to be used for status code in push notification
class PushNotification:
    INITIATED = 1
    ACCEPTED = 2
    DECLINED = 3
    COMPLETED = 4
    DELAYED = 5
    SWITCHED = 6


class SessionListStatus(Enum):

    INPROGRESS = 'in-progress'
    COMPLETED = 'completed'
    SCHEDULED = 'scheduled'
    USER_MISSED = 'user-missed'
    EXPERT_MISSED = 'expert-missed'
    CANCELLED = 'cancelled'
