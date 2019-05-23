import re
from mimetypes import guess_type

from constance import config
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.response import SimpleTemplateResponse
from django.contrib.postgres.fields import JSONField
from django.template import (
    Context,
    Template as DjangoTemplate,
)

from template.models import Template
from page.cleaners import (
    hyphenate_html,
    typograph_html,
    highlight_precode,
    wrap_hanging_punctuation,
)
from page.utils import get_base_url, PatchedFilerImageField


def wrap_meta_property(tag, property, content):
    return {
        'tag': tag,
        'attributes': {
            'property': property,
            'content': content,
        }
    }


class PageQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_published=True)

    def invisible(self):
        return self.filter(is_published=False)


class Page(models.Model):
    MAIN_PAGE_SLUG = 'main'

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
    )

    slug = models.CharField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    is_published = models.BooleanField(
        verbose_name=_('Is published'),
        default=False,
    )

    template = models.ForeignKey(
        Template,
        on_delete=models.PROTECT,
        verbose_name=_('Template')
    )

    open_graph_image = PatchedFilerImageField(
        blank=True,
        null=True,
        related_name='open_graph_image_article',
        on_delete=models.PROTECT,
        verbose_name=_('Open Graph image'),
    )

    keywords = models.CharField(
        verbose_name=_('Keywords'),
        help_text=_('Separate by comma and space'),
        max_length=255,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    seo_keywords = models.CharField(
        verbose_name=_('SEO keywords'),
        help_text=_('Separate by comma and space'),
        max_length=255,
        blank=True,
        null=True,
    )
    seo_description = models.TextField(
        verbose_name=_('SEO description'),
        blank=True,
        null=True,
    )

    meta = JSONField(
        verbose_name=_('Meta'),
        editable=False,
        blank=True,
        null=True,
    )
    clean_meta = models.TextField(
        verbose_name=_('Clean meta'),
        editable=False,
        blank=True,
        null=True,
    )

    content = models.TextField(
        verbose_name=_('Content'),
    )
    clean_content = models.TextField(
        verbose_name=_('Clean content'),
        editable=False,
        blank=True,
        null=True,
    )

    link = models.CharField(
        verbose_name=_('Link'),
        max_length=255,
        blank=True,
        null=True,
    )

    cache_link = models.TextField(
        verbose_name=_('Cache URL'),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
    )

    objects = PageQuerySet.as_manager()

    def __str__(self):
        return self.title

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.meta = self.get_meta()
        self.clean_meta = self.get_clean_meta()
        self.clean_content = self.get_clean_content()
        self.link = self.get_absolute_url()
        self.cache_link = self.get_cache_link()

    def get_absolute_url(self):
        return reverse(
            'page:visible' if self.is_published else 'page:invisible',
            kwargs={'slug': self.slug}
        )

    def get_cache_link(self):
        pattern = "{% url ['\"]page:visible['\"] ['\"]([\w+-]+)['\"] %}"
        slugs = re.findall(pattern, self.content)
        slugs.append(self.slug)  # for browser back button
        slugs.append(self.MAIN_PAGE_SLUG)  # for `main` button on page
        return reverse('page-list') + '?slug__in=' + ','.join(slugs)

    def get_base_meta(self):
        base_meta_data = {
            'keywords': self.seo_keywords,
            'description': self.seo_description,
        }
        return [
            wrap_meta_property('meta', property, content)
            for property, content in base_meta_data.items()
            if content
        ]

    def get_open_graph_meta(self):
        base_url = get_base_url()
        open_graph_data = {
            'url': base_url + self.get_absolute_url(),
            'type': 'website',
            'title': self.title,
            'locale': config.SITE_LOCALE,
            'site_name': config.SITE_NAME,
            'description': self.description,
            'determiner': '',
        }
        if self.open_graph_image:
            open_graph_data['image'] = base_url + self.open_graph_image.url
            open_graph_data['image:alt'] = self.open_graph_image.default_alt_text
            open_graph_data['image:width'] = self.open_graph_image.width
            open_graph_data['image:height'] = self.open_graph_image.height
            open_graph_data['image:type'] = guess_type(self.open_graph_image.path)[0] or ''

        return [
            wrap_meta_property('meta', 'og:' + property, content)
            for property, content in open_graph_data.items()
            if content
        ]

    def get_meta(self):
        base_meta = self.get_base_meta()
        open_graph_meta = self.get_open_graph_meta()
        return base_meta + open_graph_meta

    def get_clean_meta(self):
        html = '<meta property="meta-start" content="" />'
        for property_data in self.meta:
            attributes = [
                f'{key}="{value}"'
                for key, value in property_data['attributes'].items()
            ]
            attributes_string = ' '.join(attributes)
            html += f'<{property_data["tag"]} {attributes_string} />'
        html += '<meta property="meta-end" content="" />'
        return html

    def get_clean_content(self):
        template = DjangoTemplate(self.content)
        clean_content = template.render(Context())
        clean_content = highlight_precode(clean_content)
        clean_content = wrap_hanging_punctuation(clean_content)
        clean_content = hyphenate_html(clean_content)
        clean_content = typograph_html(clean_content)
        return clean_content
