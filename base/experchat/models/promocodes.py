from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from experchat.models.base import ExperChatBaseModel
from experchat.models.users import Expert, User


class PromoCode(ExperChatBaseModel):
    """
    Store Promo-codes Information .
    """
    ACTIVE = 1
    INACTIVE = 2
    PROMO_CODE_STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    PROMO = 'promo'
    CREDIT = 'credit'
    PROMO_CODE_TYPE_CHOICES = (
        (PROMO, 'Promo'),
        (CREDIT, 'Credit')
    )

    PERCENT_OFFER = 'percent%'
    FIXED_PRICE_OFFER = 'fixed price'
    VALUE_TYPE_CHOICES = (
        (PERCENT_OFFER, 'Percentage(%) Offer'),
        (FIXED_PRICE_OFFER, 'Fixed Price Offer')
    )

    promo_code_type = models.CharField(_('promo code type'), max_length=20, choices=PROMO_CODE_TYPE_CHOICES,)
    value_type = models.CharField(_('value type'), max_length=20, choices=VALUE_TYPE_CHOICES)
    value = models.IntegerField(_('value'))
    start_datetime = models.DateTimeField(_('start datetime'), null=True, blank=True)
    expiry_datetime = models.DateTimeField(_('expiry datetime'), null=True, blank=True)
    usage_limit = models.PositiveIntegerField(_('usage limit'), default=1)
    description = models.TextField(_('description'), max_length=500, null=True, blank=True)
    coupon_code = models.CharField(_('coupon code'), max_length=20, null=False, unique=True)
    allowed_experts = models.ManyToManyField(
        Expert,
        blank=True,
        verbose_name=_('allowed experts'),
        related_name='promo_codes',
    )
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('allowed users'),
        related_name='promo_codes',

    )
    status = models.PositiveIntegerField(_('status'), choices=PROMO_CODE_STATUS, default=ACTIVE)
    is_deleted = models.BooleanField(_('is deleted'), default=False)
    user_usage_limit = models.PositiveIntegerField(_('user usage limit'), default=1)

    class Meta:
        verbose_name = "Promo Codes"

    def __str__(self):
        return '{id}: {promo_code_type} {coupon_code}'.format(
            id=self.id if self.id else "",
            promo_code_type=self.promo_code_type,
            coupon_code=self.coupon_code
        )

    def delete(self, *args, **kwargs):
        signals.pre_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )

        self.is_deleted = True
        self.save()

        signals.post_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )
