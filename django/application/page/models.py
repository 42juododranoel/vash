import re
from mimetypes import guess_type

from constance import config
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from snippet.models import Snippet
from template.models import Template
from vash.utils import (
    PatchedFilerImageField,
    get_base_url,
)
from vash.mixins import (
    CreatedUpdatedAtMixin,
    clean_content,
)


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


class Page(CreatedUpdatedAtMixin):
    MAIN_PAGE_SLUG = 'main'

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

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
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

    open_graph_image = PatchedFilerImageField(
        blank=True,
        null=True,
        related_name='open_graph_image_article',
        on_delete=models.PROTECT,
        verbose_name=_('Open Graph image'),
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

    snippets = models.ManyToManyField(
        Snippet,
        verbose_name=_('Snippets'),
        blank=True,
        related_name='pages'
    )

    content = JSONField(
        verbose_name=_('Content'),
        editable=False,
        blank=True,
        null=True,
    )

    detail_link = models.CharField(
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

    objects = PageQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def url_name(self):
        return 'page:visible' if self.is_published else 'page:invisible'

    def get_absolute_url(self):
        return reverse(self.url_name, kwargs={'slug': self.slug})

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.content = self.get_content()
        self.cache_link = self.get_cache_link()
        self.detail_link = self.get_absolute_url()

    def _get_page_meta(self):
        return [
            wrap_meta_property('meta', property, content)
            for property, content in [
                ['keywords', self.keywords],
                ['description', self.description],
            ]
            if content
        ]

    def _get_open_graph_meta(self):
        base_url = get_base_url()
        data = {
            'url': base_url + self.get_absolute_url(),
            'type': 'website',
            'title': self.title,
            'locale': config.SITE_LOCALE,
            'site_name': config.SITE_NAME,
            'description': self.description,
            'determiner': '',
        }
        if self.open_graph_image:
            data['image'] = base_url + self.open_graph_image.url
            data['image:alt'] = self.open_graph_image.default_alt_text
            data['image:width'] = self.open_graph_image.width
            data['image:height'] = self.open_graph_image.height
            data['image:type'] = guess_type(self.open_graph_image.path)[0] or ''
        return [
            wrap_meta_property('meta', 'og:' + property, content)
            for property, content in data.items()
            if content
        ]

    def get_meta(self):
        all_meta = self._get_page_meta() + self._get_open_graph_meta()
        html = ''
        for property_data in all_meta:
            attributes = [
                f'{key}="{value}"'
                for key, value in property_data['attributes'].items()
            ]
            attributes_string = ' '.join(attributes)
            html += f'<{property_data["tag"]} {attributes_string} />'
        return html

    def get_content(self):
        content = {'meta': self.get_meta()}
        if self.id:
            m2m_queryset = self.snippets.all()
            fk_queryset = Snippet.objects.filter(page=self)
            for queryset in [m2m_queryset, fk_queryset]:
                for snippet in queryset:
                    if snippet.name in content:
                        content[snippet.name] += snippet.clean_content
                    else:
                        content[snippet.name] = snippet.clean_content
        return content

    def get_cache_link(self):
        # Run after setting `self.content`
        slugs = set()
        if 'main' in self.content:
            pattern = r'href=["\']/([\w\+-]+)["\']'
            slugs.update(re.findall(pattern, self.content['main']))
        slugs.add(self.slug)  # for browser back button
        slugs.add(self.MAIN_PAGE_SLUG)  # for `main` button on page
        return reverse('page-list') + '?slug__in=' + ','.join(slugs)
