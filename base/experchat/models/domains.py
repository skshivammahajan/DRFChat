from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.enumerations import TagTypes


class Domain(models.Model):
    """
    Store domain of expert's expertise.
    """
    name = models.CharField(_('name'), max_length=100)

    class Meta:
        db_table = "domains_domain"

    def __str__(self):
        return "{id}-{name}".format(
            id=self.id,
            name=self.name,
        )


class Tag(models.Model):
    """
    Store expert-profile's tag related to domain.
    """
    domain = models.ForeignKey(
        Domain,
        on_delete=models.PROTECT,
        verbose_name=_('tag'),
        related_name='tags',
    )
    parent = models.ForeignKey('self', null=True, related_name='tags')
    name = models.CharField(_('name'), max_length=100)
    tag_type = models.CharField(_('type'), max_length=50, choices=TagTypes.choices(), default=TagTypes.PARENT.value)

    class Meta:
        db_table = "domains_tag"
        ordering = ('domain',)

    def __str__(self):
        return "{id}-{name}".format(
            id=self.id,
            name=self.name,
        )
