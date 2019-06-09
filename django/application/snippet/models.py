from django.db import models
from django.utils.translation import ugettext_lazy as _

from vash.mixins import (
    CleanContentMixin,
    CreatedUpdatedAtMixin,
)


class Snippet(CleanContentMixin, CreatedUpdatedAtMixin):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
    )

    slug = models.CharField(
        verbose_name=_('Slug'),
        max_length=255,
    )

    page = models.ForeignKey(
        'page.Page',
        verbose_name=_('Page'),
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = ['name', 'slug']

    def __str__(self):
        return f'{self.name}-{self.slug}'
