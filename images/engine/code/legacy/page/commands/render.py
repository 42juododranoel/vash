import os
import json
from shutil import copyfile
from functools import partial

from jinja2 import (
    Environment,
    FileSystemLoader,
    Markup,
    select_autoescape,
    TemplateNotFound
)
from bs4 import BeautifulSoup

from engine.models.processors.minifier import Minifier
from legacy.constants import (
    _,
    FILES_FOLDER,
    PAGES_FOLDER,
    TEMPLATES_FOLDER,
    TAGS_TO_WRAP,
    CLASSES_TO_WRAP,
    REQUIRED_BLOCKS,
    RENDERED_JSON_FOLDER,
)
from legacy.extensions import (
    wrap_hanging_punctuation,
    typograph_html,
    hyphenate_html,
    highlight_precode,
)
from legacy.functions import RENDER_FUNCTIONS
from legacy.functions.picture import folder_path_to_url


environment = Environment(
    loader=FileSystemLoader([TEMPLATES_FOLDER, PAGES_FOLDER]),
    autoescape=select_autoescape(),
)


def sanitize_html(html):
    soup = BeautifulSoup(html, features='html.parser')

    for tag in soup.find_all():

        if tag.name in TAGS_TO_WRAP:
            wrapper_classes = [f'{tag.name}-wrapper']
            try:
                tag_classes = tag.attrs['class']
            except KeyError:
                pass
            else:
                tag_to_wrapper_classes = [
                    f'{class_}-wrapper'
                    for class_ in CLASSES_TO_WRAP
                    if class_ in tag_classes
                ]
                for class_ in tag_classes:
                    if any([class_.endswith('-below'), class_.endswith('-above')]):
                        tag_to_wrapper_classes.append(class_)
                        tag_classes.remove(class_)
                tag.attrs['class'] = tag_classes
                wrapper_classes.extend(tag_to_wrapper_classes)
            finally:
                tag.wrap(soup.new_tag('div', attrs={'class': ' '.join(wrapper_classes)}))
    else:
        soup = wrap_hanging_punctuation(soup)
        soup = highlight_precode(soup)
        html = str(soup)
        html = typograph_html(html)
        html = hyphenate_html(html)
        html = Minifier.process_content(html)
        return html


def render(slug, page_meta, template_name, no_images=False):
    # Prepare render context
    render_context = RENDER_FUNCTIONS.copy()
    if no_images:
        render_context['picture'] = partial(render_context['picture'], dry_run=True)

    render_context['picture'] = partial(
        render_context['picture'],
        page_slug=slug,  # Template tag needs page slug to make image paths
    )

    related_page_slugs = []  # Will be used to make JSON for seamless cache
    render_context['link'] = partial(
        render_context['link'],
        related_page_slugs=related_page_slugs,
    )

    render_context.update(page_meta['variables'])

    # Prepare extensions
    for extension in page_meta.get('extensions', []):
        if extension == 'opengrapher':
            og_image_name = page_meta['variables']['og_image']
            og_image_folder = f'{FILES_FOLDER}/{slug}'
            os.makedirs(og_image_folder, exist_ok=True)

            old_image_path = f'{PAGES_FOLDER}/{slug}/images/{og_image_name}'
            new_image_path = f'{og_image_folder}/{og_image_name}'
            copyfile(old_image_path, new_image_path)
            print(f'Processing OG image“{og_image_name}”...')
            render_context['og_image'] = folder_path_to_url(new_image_path)

            render_context['og_url'] = f'{page_meta["variables"]["site_url"]}/{slug}'
            render_context['og_title'] = page_meta['title']
            render_context['og_type'] = page_meta['variables']['og_type']
            render_context['og_locale'] = page_meta['variables']['og_locale']
            render_context['og_site_name'] = page_meta['variables']['og_site_name']

    # Get template and render page as HTML
    template = environment.get_template(f'_default.html')
    rendered_html_content = template.render(**render_context, **blocks)
    rendered_html_content = sanitize_html(rendered_html_content)

    # Render page and related pages as JSON for seamless cache
    json_blocks = {
        block_name: sanitize_html(blocks[block_name])
        for block_name in blocks.keys()
        if block_name in REQUIRED_BLOCKS
    }

    json_blocks['scripts'] = []
    for script_data in page_meta.get('scripts', []):
        script_data['defer'] = 'defer'
        json_blocks['scripts'].append(script_data)

    key = f'/{slug}' if slug != 'index' else '/'
    json_data = {
        key: {
            'title': page_meta['title'],
            'blocks': json_blocks,
        }
    }
    for related_page_slug in related_page_slugs:
        print(f'  Processing related page “{related_page_slug}”')
        with open(f'{RENDERED_JSON_FOLDER}/{related_page_slug}.json') as file:
            related_page_link = f'/{related_page_slug}' if related_page_slug != 'index' else '/'
            json_data[related_page_link] = json.load(file)[related_page_link]
    rendered_json_content = json.dumps(json_data)

    return rendered_html_content, rendered_json_content
