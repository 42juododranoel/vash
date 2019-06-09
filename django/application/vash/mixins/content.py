from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template

from vash.cleaners import (
    hyphenate_html,
    typograph_html,
    highlight_precode,
    wrap_hanging_punctuation,
)


def clean_content(content):
    template = Template(content)
    clean_content = template.render(Context())
    clean_content = highlight_precode(clean_content)
    clean_content = wrap_hanging_punctuation(clean_content)
    clean_content = typograph_html(clean_content)
    clean_content = hyphenate_html(clean_content)
    return clean_content


class CleanContentMixin(models.Model):
    content = models.TextField(
        verbose_name=_('Content'),
    )
    clean_content = models.TextField(
        verbose_name=_('Clean content'),
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_content = self.get_clean_content()

    def get_clean_content(self):
        return clean_content(self.content)
