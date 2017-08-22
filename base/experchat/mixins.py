from django.db import models
from django.utils.translation import ugettext_lazy as _


class SoftDeleteMixin:
    """
    Provide django model functionality of soft delete.
    """
