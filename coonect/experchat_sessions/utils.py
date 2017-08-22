import datetime
import logging

from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.utils import timezone

from experchat.models.promocodes import PromoCode
from experchat.utils import filter_slots, get_booked_and_available_slots
from experchat_sessions.models import Session, SessionEvent
from payments.models import Transaction

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SessionEventsProcess(object):
    """
    This utility class handles six cases of webrtc events.

    For detailed doc please click on below link:
    https://experchat.atlassian.net/wiki/display/WED/WebRTC+Callback+Events+Listing
    """

    def __init__(self, req_data):
        self.event_data = req_data

    def unix_to_datetime(self, unix_time):
        return datetime.datetime.fromtimestamp(
            int(unix_time)/1000).strftime('%Y-%m-%d %H:%M:%S')

    def process_events(self):
        se = SessionEvent()
        se.event_data = self.event_data
        se.session_id = self.event_data.get('sessionId')
        timestamp = self.event_data.get('timestamp')
        se.timestamp = self.unix_to_datetime(timestamp)
        se.event = self.event_data.get('event')
        se.event_reason = self.event_data.get('reason')

        if not self.event_data.get('connection') and not self.event_data.get('stream'):
            logger.error("Webhook event: {} not implemented.".format(se.event))
            return

        if self.event_data.get('stream'):
            se.connection_id = self.event_data.get('stream').get('connection')['id']
            event_created_at = self.event_data.get('stream')['createdAt']
            se.event_date_time = self.unix_to_datetime(event_created_at)
            se.save()
            return

        elif self.event_data.get('connection'):
            se.connection_id = self.event_data.get('connection')['id']
            event_date_time = self.event_data.get('connection')['createdAt']
            se.event_date_time = self.unix_to_datetime(event_date_time)

            se.save()

            if self.event_data.get('event') == 'connectionDestroyed':
                session_event_data = SessionEvent.objects.filter(
                    session_id=se.session_id
                ).values()
                connection_destroyed_count = 0
                connection_created_count = 0
                stream_created_time = ''
                stream_destroyed_time = ''
                for data in session_event_data:
                    if data['event'] == 'connectionDestroyed':
                        connection_destroyed_count += 1
                    elif data['event'] == 'connectionCreated':
                        connection_created_count += 1
                    elif not stream_created_time and data['event'] == 'streamCreated':
                        stream_created_time = data['event_date_time']
                    elif data['event'] == 'streamDestroyed':
                        stream_destroyed_time = data['event_date_time']

                if connection_created_count == connection_destroyed_count:
                    time_diff = (stream_destroyed_time - stream_created_time)
                    time_in_minutes = time_diff.total_seconds()/60.0

                    session_data = Session.objects.get(tokbox_session_id=se.session_id)
                    if not session_data.tokbox_session_length:
                        session_data.tokbox_session_length = round(time_in_minutes)
                        session_data.save()


def is_already_scheduled(user, start_date_time, duration):
    """
    This util method is used to check if User is booked with the same slots for any expert then we need to show
    the error message
    Args:
        user (object) : user
        start_date_time (obj): datetime
        duration (int): duration of the session
    return:
        Returns True if there are any slots available within the passed interval otherwise false
    """
    end_date_time = start_date_time + timezone.timedelta(minutes=duration)
    craeted_sessions = Session.objects.filter(user=user).filter(is_deleted=False).annotate(
        endtime=RawSQL("ADDDATE(`scheduled_datetime`, INTERVAL `scheduled_duration` MINUTE)", tuple())).filter(
        Q(scheduled_datetime__gte=start_date_time,
          scheduled_datetime__lte=end_date_time) |
        Q(endtime__gt=start_date_time,
          endtime__lt=end_date_time)).exists()

    if craeted_sessions:
        return True
    return False


def is_valid_scheduled_slot(expert_id, start_date_time, duration):
    available_slots, booked_slots = get_booked_and_available_slots(expert_id)
    filtered_slots = filter_slots(available_slots, booked_slots)

    end_date_time = start_date_time + timezone.timedelta(minutes=duration)
    for slot in filtered_slots:
        if start_date_time >= slot['start_time'] and end_date_time <= slot['end_time']:
            return True
    return False


def is_valid_promocode(user, promo_code, expert_id, schedule_datetime):
    """
    Util method to validate the promo code
    Args:
        promo_code (string): Promo code
        expert_id (id): expert id
        schedule_datetime (Datetime): Schedule date time
    return:
        Boolean and price of the promo code
    """
    is_valid_promo_code = False
    promo_code_obj = PromoCode.objects.filter(coupon_code=promo_code).first()
    # check if promo code is available
    if promo_code_obj is None:
        return is_valid_promo_code

    # check if the promo code is active
    if promo_code_obj.status == PromoCode.INACTIVE:
        return is_valid_promo_code

    # check if the promocode is expired or still not active
    if promo_code_obj.expiry_datetime and (
            promo_code_obj.expiry_datetime < schedule_datetime or promo_code_obj.start_datetime > schedule_datetime):
        return is_valid_promo_code

    # check if the coupan code is applicable for the passed expert, otherwise global coupan code
    allowed_experts_ids = [code.userbase_id for code in promo_code_obj.allowed_experts.all()]
    if allowed_experts_ids and (expert_id not in allowed_experts_ids):
        return is_valid_promo_code

    # check if the coupan code is applicable for the passed user, otherwise global coupan code
    allowed_user_ids = [code.userbase_id for code in promo_code_obj.allowed_users.all()]
    if allowed_user_ids and (user.userbase_id not in allowed_user_ids):
        return is_valid_promo_code

    # Validate the coupan code based on Transaction table
    return validate_coupon_code_amount_used(promo_code_obj)


def calculate_used_promo_code_amount(promo_code_transactions):
    """
    Util method to calulate the already applied promo codes amounts
    Args:
        promo_code_transactions (obj): Transactions
    return:
        Sum of all amount used
    """
    # TODO use here queryset to get the SUM
    total_amount_used = 0
    for transaction in promo_code_transactions:
        total_amount_used += transaction.amount

    return total_amount_used


def validate_coupon_code_amount_used(promo_code_obj):
    """
    Method to validate the promocode amount based on Transaction table
    Args:
        promo_code_obj (obj): PromoCode
    return:
        Boolean (True or False): True if promo code can be applied other wise False
    """
    # get the transaction related to the promo code
    promo_code_transactions = promo_code_obj.transactions.all().filter(
        status__in=[Transaction.UNSETTLED, Transaction.SETTLED]
    )
    if promo_code_transactions:
        # in both cases count will be the max used limit
        if promo_code_transactions.count() >= promo_code_obj.usage_limit:
            return False
        # if user limit is consumed then raise the exception
        if promo_code_transactions.count() >= promo_code_obj.user_usage_limit:
            return False
        # in case of credit amount will be also need to be calculated
        if promo_code_obj.promo_code_type == PromoCode.CREDIT:
            total_amount_used = calculate_used_promo_code_amount(promo_code_transactions)
            if total_amount_used >= promo_code_obj.value:
                return False

    return True


def calculate_discount_price(promo_code, session_price):
    """
    Calculate the discount price for the provided promo code, considering already applied promo code
    Here in case of Credit type we will be considering the already Schduled and Settled Transactions
    But in case of Promo we don't need to worry about Already scheduled Sessions only limit will be considered

    Args:
        promo_code (string): promo code
        session_price (object): Session price
    return:
        discount price from promo code
    """
    promo_code_obj = PromoCode.objects.filter(coupon_code=promo_code).first()
    # in case of Credit type we need to calculate the exact amount which can be used by looking in the Scheduled or
    # Completed transaction
    used_amount = 0
    if promo_code_obj.promo_code_type == PromoCode.CREDIT:
        promo_code_transactions = promo_code_obj.transactions.all().filter(
            status__in=[Transaction.UNSETTLED, Transaction.SETTLED]
        )
        if promo_code_transactions:
            used_amount = calculate_used_promo_code_amount(promo_code_transactions)

    if promo_code_obj.value_type == PromoCode.PERCENT_OFFER:
        discount_price = round((session_price * promo_code_obj.value) / 100)
    else:
        discount_price = promo_code_obj.value

    if used_amount > 0:
        remaining_promo_code_amount = promo_code_obj.value - used_amount
        if remaining_promo_code_amount > discount_price:
            return discount_price
        return remaining_promo_code_amount

    return discount_price
