from django.db import models
from django.utils.translation import ugettext_lazy as _


class ExperChatBaseModel(models.Model):
    created_timestamp = models.DateTimeField(_('created timestamp'), auto_now_add=True)
    modified_timestamp = models.DateTimeField(_('modified timestamp'), auto_now=True)

    class Meta:
        abstract = True
