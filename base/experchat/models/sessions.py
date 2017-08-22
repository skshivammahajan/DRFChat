from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from experchat.enumerations import CallStatus, DeviceStatus
from experchat.models.base import ExperChatBaseModel
from experchat.models.promocodes import PromoCode
from experchat.models.users import Expert, ExpertProfile


class EcDevice(ExperChatBaseModel):
    """
    Store user's devices to send push notifications to.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device_name = models.CharField(_('Device Name'), max_length=50)
    device_type = models.CharField(_('Device Type'), max_length=20, db_index=True)
    device_sub_type = models.CharField(_('Device Subtype'), max_length=20)
    device_id = models.CharField(
        _('Device Id'),
        max_length=128,
        db_index=True,
        null=True,
        blank=True
    )
    device_token = models.CharField(_('Device Token'), max_length=255, db_index=True)
    device_os = models.CharField(_('Device Os'), max_length=50)
    status = models.PositiveSmallIntegerField(
        _('Device Status'),
        default=DeviceStatus.ACTIVE.value,
        choices=DeviceStatus.choices()
    )

    class Meta:
        db_table = "devices_device"
        ordering = ['-created_timestamp']

    def __str__(self):
        return self.device_name

    def delete(self, *args, **kwargs):
        signals.pre_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )

        self.status = DeviceStatus.INACTIVE.value
        self.save()


class EcSession(ExperChatBaseModel):
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    expert_profile = models.ForeignKey(
        ExpertProfile,
        on_delete=models.PROTECT,
        verbose_name=_("Expert Profile Id")
    )
    expert = models.ForeignKey(
        Expert,
        on_delete=models.PROTECT,
        verbose_name=_("Expert Id"),
    )
    expert_device = models.ForeignKey(
        EcDevice,
        on_delete=models.PROTECT,
        verbose_name=_("Expert Device"),
        related_name='expert_device_sessions',
        null=True,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_device = models.ForeignKey(
        EcDevice,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_("User Device"),
        related_name='user_device_sessions',
    )
    tokbox_session_id = models.CharField(max_length=100)
    tokbox_session_length = models.IntegerField(default=0, help_text='Total session time (in seconds).')
    scheduled_duration = models.IntegerField(_("Scheduled Duration"), default=10)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.0000'))
    title = models.CharField(max_length=100, null=True, blank=True)
    call_status = models.PositiveIntegerField(
        default=CallStatus.INITIATED.value,
        choices=CallStatus.choices()
    )
    details = models.TextField(_("Session Detail"), max_length=500, default='', blank=True, null=True)
    scheduled_datetime = models.DateTimeField(_("call schedule datetime"), default=timezone.now)
    is_deleted = models.BooleanField(_('is deleted'), default=False)
    extended_duration = models.IntegerField(_("Extended Duration"), default=0)
    estimated_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.0000'))
    card = models.PositiveIntegerField('card', null=True, blank=True)
    promo_code = models.CharField(_('promo code'), max_length=20, null=True, blank=True)

    class Meta:
        db_table = "experchat_sessions_session"
        ordering = ['-start_timestamp']

    def __str__(self):
        return "Call id {0} .".format(self.id)+"Expert id {0}.".format(self.expert_id)

    def delete(self, *args, **kwargs):
        models.signals.pre_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )

        self.is_deleted = True
        self.save()

        models.signals.post_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )
