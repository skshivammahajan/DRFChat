from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.models.base import ExperChatBaseModel
from experchat.models.promocodes import PromoCode


class Customer(ExperChatBaseModel):
    """
    Store payement gateway customer details.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='customers'
    )
    customer_uid = models.CharField(_('customer uid'), max_length=50)
    gateway = models.IntegerField(_('gateway'), default=1)

    def __str__(self):
        return "{user}: {customer_uid}".format(
            user=self.user,
            customer_uid=self.customer_uid,
        )


class Card(ExperChatBaseModel):
    """
    Store the card details of a customer.
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
        related_name='cards'
    )
    last_4 = models.CharField(_('last 4 digits of card'), max_length=4)
    is_default = models.BooleanField(_('is default'), default=False)
    payment_method_token = models.CharField(_('payment method token'), max_length=50)
    expiration_date = models.CharField(_('expiration date'), max_length=7)
    card_type = models.CharField(_('card type'), max_length=50)

    def __str__(self):
        return "{user}: {last_4}".format(
            user=self.customer.user,
            last_4=self.last_4,
        )


class Transaction(ExperChatBaseModel):
    """
    Store the transaction details of a user.
    """
    UNSETTLED = 1
    SETTLED = 2
    CANCELLED = 3
    FAILED = 4

    TRANSACTION_STATUSES = (
        (UNSETTLED, 'Unsettled Transaction'),
        (SETTLED, 'Settled Transaction'),
        (CANCELLED, 'Cancelled Transaction'),
        (FAILED, 'Failed Transaction'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='transactions',
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        verbose_name=_('user'),
        related_name='transactions',
        null=True,
    )
    transaction_uid = models.CharField(_('transaction uid'), max_length=50)
    status = models.PositiveSmallIntegerField(_('status'), choices=TRANSACTION_STATUSES, default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.0000'))
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        verbose_name=_('promo_code'),
        related_name='transactions',
        null=True
    )

    def __str__(self):
        return "{user}: {amount} {status}".format(
            user=self.user,
            amount=self.amount,
            status=self.status,
        )
