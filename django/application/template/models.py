from django.db import models
from filer.fields.file import FilerFileField
from django.utils.translation import ugettext_lazy as _


class Template(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
    )

    file = FilerFileField(
        verbose_name=_('File'),
        on_delete=models.PROTECT,
        related_name='file_template'
    )

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.name
