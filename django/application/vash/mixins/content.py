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
    content_cleaned = template.render(Context())
    content_cleaned = highlight_precode(content_cleaned)
    content_cleaned = wrap_hanging_punctuation(content_cleaned)
    content_cleaned = typograph_html(content_cleaned)
    content_cleaned = hyphenate_html(content_cleaned)
    return content_cleaned


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
