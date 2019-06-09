from mimetypes import guess_type

from bs4 import BeautifulSoup
from django.conf import settings
from filer.models import File
from django.utils.html import mark_safe
from easy_thumbnails.files import get_thumbnailer
from django.template.defaulttags import register

from vash.utils import get_html_formatter


@register.simple_tag
def render_svg(file_id):
    filer_file = File.objects.get(id=file_id)
    with open(filer_file.path, 'r') as file:
        file_content = file.read()
    soup = BeautifulSoup(file_content, 'html')
    svg = soup.find('svg')
    return mark_safe(str(svg))


@register.simple_tag
def render_file_url(file_id):
    file = File.objects.get(id=file_id)
    return mark_safe(file.url)


@register.simple_tag
def render_code_style():
    formatter = get_html_formatter()
    css = formatter.get_style_defs()
    return mark_safe(css)


@register.simple_tag
def render_picture(file_id, classes='', is_gif=False):
    image = File.objects.get(id=file_id)
    thumbnailer = get_thumbnailer(image.path)

    html = '<picture>'
    if not is_gif:
        for source_key in settings.THUMBNAIL_PICTURE_SOURCES:
            thumbnail_image = thumbnailer[source_key]
            thumbnail_width = settings.THUMBNAIL_ALIASES[''][source_key]['size'][0]
            thumbnail_mimetype = guess_type(thumbnail_image.path)[0]
            thumbnail_url = thumbnail_image.url.replace(settings.MEDIA_ROOT, '')

            source_tag = '<source media="(max-width: {}px)" srcset="{}"'
            source_tag = source_tag.format(thumbnail_width, thumbnail_url)
            if thumbnail_mimetype:
                source_tag += f' type="{thumbnail_mimetype}" />'
            else:
                source_tag += ' />'
            html += source_tag

    default_classes = 'lazy'
    classes = ' '.join([default_classes, classes])

    img_tag = f'<img class="{classes}" data-src="{image.url}"'
    if image.default_alt_text:
        img_tag += f' alt="{image.default_alt_text}" />'
    else:
        img_tag += ' />'
    html += img_tag
    html += '</picture>'
    return mark_safe(html)
