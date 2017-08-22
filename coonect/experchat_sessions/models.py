from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django_mysql.models import JSONField

from experchat.enumerations import CallStatus
from experchat.models.base import ExperChatBaseModel
from experchat.models.sessions import EcSession
from experchat_sessions import tasks
from experchat_sessions.enumerations import PushNotification
from payments.models import Transaction
from publisher.utils import ExperchatPublisher, publish_data
from webrtc.utils import ExperchatWebRTC


class Session(EcSession):

    class Meta:
        proxy = True

    def publish_info(self, user_type, session_info, alert, user_id=None):
        if not user_id:
            user_id = self.user_id
        pubnub_publish_data = publish_data(session_info, alert)
        ExperchatPublisher().publish_message_on_user_devices(
            user_id,
            user_type,
            pubnub_publish_data
        )

    def publish_device_info(self, user_type, device_id, session_info, alert):
            pubnub_publish_data = publish_data(session_info, alert)
            ExperchatPublisher().publish_message_on_device(
                user_type=user_type,
                device_id=device_id,
                message=pubnub_publish_data
            )

    def initialize(self):
        date_time = str(int(timezone.now().timestamp()))

        self.call_status = CallStatus.INITIATED.value
        self.save()

        def get_init_call_data_dict():
            return {
                'user_id': self.user.id,
                'display_name': self.user.user.display_name,
                'profile_photo': self.user.profile_photo,
                'user_device_id': self.user_device.id,
                'call_id': self.id,
                'timestamp': date_time,
                'status': PushNotification.INITIATED,
                'title': self.title,
            }

        session_info = get_init_call_data_dict()
        user_id = self.expert.id
        user_type = 'expert'
        alert = _("User Calling ...")

        pubnub_publish_data = publish_data(session_info, alert)

        ExperchatPublisher().publish_message_on_user_devices(
            user_id,
            user_type,
            pubnub_publish_data
        )

    def reconnect(self):
        """
        Reconnect call if:
        1. session was not cancelled or
        2. it is not in scheduled status or
        3. scheduled duration is not elapse
        """
        if self.is_deleted or self.call_status == CallStatus.SCHEDULED.value or \
                timezone.now() >= self.scheduled_datetime + timezone.timedelta(minutes=self.scheduled_duration):
            return
        date_time = str(int(timezone.now().timestamp()))

        self.call_status = CallStatus.INITIATED.value
        self.save()

        def get_reconnect_call_data_dict():
            return {
                'user_id': self.user.id,
                'display_name': self.user.user.display_name,
                'profile_photo': self.user.profile_photo,
                'user_device_id': self.user_device.id,
                'call_id': self.id,
                'timestamp': date_time,
                'status': PushNotification.INITIATED,
                'title': self.title,
            }

        session_info = get_reconnect_call_data_dict()

        self.publish_device_info('expert', self.user_device.id, session_info, _("User Calling ..."))

    def decline_call(self):
        if self.call_status != CallStatus.INITIATED.value:
            return

        self.call_status = CallStatus.DECLINED.value
        self.end_timestamp = timezone.now()
        self.save()

        def get_decline_call_data_dict():
            return {
                'user_name': self.expert.userbase.name,
                'user_id': self.expert.id,
                'call_id': self.id,
                'timestamp': str(int(timezone.now().timestamp())),
                'status': PushNotification.DECLINED
            }

        session_info = get_decline_call_data_dict()
        self.publish_device_info('user', self.user_device.id, session_info, _('Call declined ...'))

    def delay_call(self, delay_time):
        if self.call_status != CallStatus.INITIATED.value:
            return

        self.call_status = CallStatus.DELAYED.value
        self.end_timestamp = timezone.now()
        self.save()

        def get_delay_call_data_dict():
            return {
                'user_name': self.expert.userbase.name,
                'user_id': self.expert_id,
                'call_id': self.id,
                'timestamp': str(int(timezone.now().timestamp())),
                'delay_duration': delay_time,
                'status': PushNotification.DELAYED
            }

        session_info = get_delay_call_data_dict()
        self.publish_device_info('user', self.user_device.id, session_info, _('Call delayed ...'))

    def accept_call(self, expert_device):
        if self.call_status != CallStatus.INITIATED.value:
            return

        if not self.tokbox_session_id:
            self.tokbox_session_id = ExperchatWebRTC().get_webrtc_session()

        session_token = ExperchatWebRTC().get_webrtc_session_token(self.tokbox_session_id)

        self.expert_device = expert_device
        self.call_status = CallStatus.ACCEPTED.value
        self.start_timestamp = timezone.now()
        self.save()

        def get_accept_call_data_dict():
            return {
                'seesion_id': self.tokbox_session_id,
                'session_token': session_token,
                'status': PushNotification.ACCEPTED,
                'timestamp': str(int(timezone.now().timestamp())),
                'apiKey': settings.TOKBOX_API_KEY,
                'call_timeout': settings.TOKBOX_CALL_TIMEOUT,
                'expert_device': expert_device.id,
                'title': self.title,
            }

        session_info = get_accept_call_data_dict()
        self.publish_device_info('user', self.user_device.id, session_info, _('Call accepted ...'))
        return session_info

    def disconnect_call(self, initiator, tokbox_session_length):
        if self.call_status not in [CallStatus.ACCEPTED.value, CallStatus.INITIATED.value]:
            return

        self.call_status = CallStatus.COMPLETED.value
        self.end_timestamp = timezone.now()

        if self.tokbox_session_length == 0:
            self.tokbox_session_length = tokbox_session_length

        # Fix if, user extended session but didn't continued call.
        self.fix_extended_duration()

        if self.tokbox_session_length > settings.SESSION_MIN_DURATION_FOR_STATS:
            self.revenue = self.calculate_session_revenue()
            tasks.calculate_daily_expert_session_stats.delay(self.expert.id, self.revenue)
            tasks.apply_payments_for_completed_session.delay(self.id, self.revenue)
        self.save()

        def get_disconnect_call_data_dict(initiator_id, user_name):
            return {
                'user_name': user_name,
                'user_id': initiator_id,
                'call_id': self.id,
                'timestamp': str(int(timezone.now().timestamp())),
                'status': PushNotification.COMPLETED,
                'tokbox_session_length': self.tokbox_session_length,
                'revenue': float(self.revenue),
            }

        if initiator == 'user':
            if self.expert_device is None:
                user_type = 'expert'
                user_id = self.expert.id
                session_info = get_disconnect_call_data_dict(user_id, _(self.user.name))
                self.publish_info(
                    user_type,
                    session_info,
                    _('Disconnect call ...'),
                    user_id)
                return session_info
            else:
                user_type = 'expert'
                device_id = self.expert_device.id
                session_info = get_disconnect_call_data_dict(self.user.id, _(self.user.name))

        elif initiator == 'expert':
            user_type = 'user'
            device_id = self.user_device.id
            session_info = get_disconnect_call_data_dict(self.expert.id, _(self.expert.userbase.name))

        self.publish_device_info(
            user_type=user_type,
            device_id=device_id,
            session_info=session_info,
            alert=_('Disconnect call ...'),
        )

    def switch_device(self, device_id):
        tokbox_token = ExperchatWebRTC().get_webrtc_session_token(
            self.tokbox_session_id
        )

        def get_switch_call_data_dict():
            return {
                'seesion_id': self.tokbox_session_id,
                'session_token': tokbox_token,
                'status': PushNotification.SWITCHED,
                'timestamp': str(int(timezone.now().timestamp())),
                'apiKey': settings.TOKBOX_API_KEY,
                "call_timeout": settings.TOKBOX_CALL_TIMEOUT,
            }

        session_info = get_switch_call_data_dict()
        self.publish_device_info(
            user_type='expert',
            device_id=device_id,
            session_info=session_info,
            alert=_('Call switched ...')
        )
        return session_info

    def extend_session(self):
        self.extended_duration = self.extended_duration + settings.SESSION_EXTENSION_TIME
        self.save()

    def cancel_session(self):
        tasks.cancel_payment_on_session_cancellation.delay(self.id)
        self.is_deleted = True
        self.save()

    def calculate_session_revenue(self):
        revenue = self.estimated_revenue

        if self.tokbox_session_length <= settings.SESSION_MIN_DURATION_FOR_REVENUE:
            return 0

        # If user has not extended session
        if self.tokbox_session_length <= self.scheduled_duration * 60:
            return revenue

        # extension_count * per_extension_price
        extension_price = (self.extended_duration/settings.SESSION_EXTENSION_TIME) * settings.SESSION_EXTENSION_PRICE

        return float(revenue) + extension_price

    def fix_extended_duration(self):
        """
        Consider per session extension time = 10
        Case 1:
            actual_extended_time = 29
            extended_duration = 30
            Decision: Do nothing
        Case 2:
            actual_extended_time = 29
            extended_duration = 40
            Decision: User should be charged for 30 as User wanted to extend but didn't.
            Fix extended_duration to 40 - 10
        """
        actual_extended_time = self.tokbox_session_length - self.scheduled_duration*60
        difference_of_extended_times = self.extended_duration - actual_extended_time
        if difference_of_extended_times > settings.SESSION_EXTENSION_TIME:
            self.extended_duration -= settings.SESSION_EXTENSION_TIME


class SessionEvent(ExperChatBaseModel):
    """
    Store session event's data.
    """
    session_id = models.CharField(_("Session ID"), max_length=100, null=False)
    event = models.CharField(_("Event"), max_length=50, null=False)
    event_date_time = models.DateTimeField(_("Event Date Time"))
    connection_id = models.CharField(_("Connection ID"), max_length=100, null=False)
    event_reason = models.CharField(_("Reason"), max_length=200, null=True, blank=True)
    event_data = JSONField(_("Event Data"))

    def __str__(self):
        return "Session ID : {session_id}. Event : {event}".format(session_id=self.session_id, event=self.event)


class SessionTransaction(ExperChatBaseModel):
    """
    Store transaction details of a session.
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='session')
    session_event_type = models.CharField('session event type', max_length=50, default='')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name='transaction')

    def __str__(self):
        return "Session ID : {session}, Transaction ID : {transaction}".format(session=self.session,
                                                                               transaction=self.transaction)
