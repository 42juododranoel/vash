import os
from shutil import copyfile

from jinja2 import Markup

from legacy.processor import ImageProcessor

FILES_URL = '/files'

FILES_FOLDER = '/resources/files'
PAGES_FOLDER = '/resources/pages'
TEMPLATES_FOLDER = '/resources/templates'

RENDERED_HTML_FOLDER = f'/resources/assets/html'
RENDERED_JSON_FOLDER = f'/resources/assets/json'

TAGS_TO_WRAP = ['p', 'h1', 'h2', 'h3', 'figcaption', 'ul', 'ol']
CLASSES_TO_WRAP = ['subscription', 'medium-heading', 'indent']

SLUG_HELP_TEXT = '0-9, a-z, A-Z, -, _.'
REQUIRED_BLOCKS = ['meta', 'styles', 'body']

FRONTEND_BREAKPOINT_SM = 0
FRONTEND_BREAKPOINT_MD = 960
FRONTEND_BREAKPOINT_LG = 1400
FRONTEND_COLUMNS_COUNT = 16


def folder_path_to_url(path):
    # /resources/files/samurai/oda_nobutaka_1565772464_1660.webp
    # → /files/samurai/oda_nobutaka_1565772464_1660.webp
    return path.replace(FILES_FOLDER, FILES_URL, 1)


def picture(file_name, context, dry_run=False, alt_text='', image_classes='', wrapper_classes='', is_borderless=False, col_sm=None, col_md=None, col_lg=None):
    """
    Output complex HTML with “picture” and “.picture-wrapper”
    """

    page_slug = context['page'].path

    col_sm = col_sm or FRONTEND_COLUMNS_COUNT
    col_md = col_md or col_sm
    col_lg = col_lg or col_md

    size_sm = 100 / FRONTEND_COLUMNS_COUNT * col_sm
    size_md = 100 / FRONTEND_COLUMNS_COUNT * col_md
    size_lg = 100 / FRONTEND_COLUMNS_COUNT * col_lg

    sizes = f'(min-width: {FRONTEND_BREAKPOINT_LG}px) {size_lg}vw, '
    sizes += f'(min-width: {FRONTEND_BREAKPOINT_MD}px) {size_md}vw, '
    sizes += f'{size_sm}vw'

    image_folder_new = f'{FILES_FOLDER}/{page_slug}/{file_name.split(".")[0]}'
    os.makedirs(image_folder_new, exist_ok=True)

    image_path_old = f'{PAGES_FOLDER}/{page_slug}/images/{file_name}'
    image_path_new = f'{image_folder_new}/{file_name.split("/")[-1]}'
    if not os.path.isfile(image_path_new):
        copyfile(image_path_old, image_path_new)
        print(f'Processing “{file_name}”...')
    else:
        print(f'Image “{file_name}” already exists, forcing dry run')
        dry_run = True

    image_processor = ImageProcessor(image_path_new)
    if dry_run:
        thumbnails = image_processor.get_thumbnails(can_create_files=False, can_delete_old=False)
    else:
        thumbnails = image_processor.get_thumbnails(can_create_files=True, can_delete_old=True)

    make_srcset = lambda srcs: ', '.join(
        [
            f'{folder_path_to_url(src["path"])} {src["width"]}w'
            for src in srcs
        ]
    )

    image_width = image_processor.image_width
    image_height = image_processor.image_height

    base_classes = ['picture-wrapper']
    if image_processor.is_image_transparent:
        base_classes.append('picture-wrapper-transparent')
    if is_borderless:
        base_classes.append('picture-wrapper-borderless')
    wrapper_classes = ' '.join(base_classes)

    wrapper_outer_style = f'padding-bottom: {round(image_height / image_width * 100, 2)}%'

    html = f'<div class="{wrapper_classes}" style="max-width: {image_width}px">'
    html += f'<div class="picture-wrapper-outer" style="{wrapper_outer_style}">'
    html += f'<div class="picture-wrapper-inner">'
    html += '<picture>'

    for mimetype, srcs in thumbnails['sources'].items():
        html += f'<source type="{mimetype}" srcset="{make_srcset(srcs)}" sizes="{sizes}"/>'

    data_srcset = make_srcset(thumbnails['image'])
    image_classes = f'lazy {image_classes}' if image_classes else 'lazy'
    data_src = folder_path_to_url(image_path_new)
    alt_text = f' alt="{alt_text}"' if alt_text else ''
    html += (
        f'<img width="{image_width}" '
        f'data-srcset="{data_srcset}" '
        f'data-sizes="{sizes}" '
        f'class="{image_classes}" '
        f'data-src="{data_src}"'
        f'{alt_text}/>'
    )

    html += '</picture></div></div></div>'
    return Markup(html)
