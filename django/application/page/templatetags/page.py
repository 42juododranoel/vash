from django.template.defaulttags import register

from page.models import Page
from page.rest import PageSerializer


@register.simple_tag
def get_page(slug):
    page = Page.objects.get(slug)
    serialized_page = PageSerializer(page)
    return serialized_page
