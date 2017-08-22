from django.db import models
from django.utils.translation import ugettext as _

from experchat.models.base import ExperChatBaseModel


class SessionPricing(ExperChatBaseModel):
    session_length = models.PositiveIntegerField(_("session length"), default=0)
    price = models.PositiveIntegerField(_("session price"), default=0)

    def __str__(self):
        return "{session_length}M: {price}$".format(
            session_length=self.session_length,
            price=self.price
        )
