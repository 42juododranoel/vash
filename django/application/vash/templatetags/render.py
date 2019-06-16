from mimetypes import guess_type

from bs4 import BeautifulSoup
from constance import config
from django.conf import settings
from filer.models import File
from django.utils.html import mark_safe
from easy_thumbnails.files import get_thumbnailer
from django.template.defaulttags import register

from vash.utils import (
    ImageProcessor,
    media_path_to_url,
    get_html_formatter,
)


@register.simple_tag
def picture(file_id, classes='', col_sm=None, col_md=None, col_lg=None):
    col_sm = col_sm or config.FRONTEND_COLUMNS_COUNT
    col_md = col_md or col_sm
    col_lg = col_lg or col_md

    size_sm = 100 / config.FRONTEND_COLUMNS_COUNT * col_sm
    size_md = 100 / config.FRONTEND_COLUMNS_COUNT * col_md
    size_lg = 100 / config.FRONTEND_COLUMNS_COUNT * col_lg

    image = File.objects.get(id=file_id)
    image_processor = ImageProcessor(image)
    picture_structure = image_processor.get_picture_structure()

    sizes = f'(min-width: {config.FRONTEND_BREAKPOINT_LG}px) {size_lg}vw, '
    sizes += f'(min-width: {config.FRONTEND_BREAKPOINT_MD}px) {size_md}vw, '
    sizes += f'{size_sm}vw'

    make_srcset = lambda srcs: ', '.join(
        [f'{media_path_to_url(src["path"])} {src["width"]}w' for src in srcs]
    )

    html = '<picture>'
    for mimetype, srcs in picture_structure['sources'].items():
        html += '<source type="{}" srcset="{}" sizes="{}"/>'.format(
            mimetype, make_srcset(srcs), sizes
        )

    html += '<img width="{}" data-srcset="{}" data-sizes="{}" class="{}" data-src="{}"{}/>'.format(
        image.width,
        make_srcset(picture_structure['image']),
        sizes,
        f'lazy {classes}' if classes else 'lazy',
        image.url,
        f' alt="{image.default_alt_text}"' if image.default_alt_text else '',
    )
    html += '</picture>'
    return mark_safe(html)


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
