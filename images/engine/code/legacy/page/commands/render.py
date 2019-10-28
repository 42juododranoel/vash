import json
from functools import partial

from bs4 import BeautifulSoup

from engine.models.processors.minifier import Minifier
from legacy.constants import (
    TAGS_TO_WRAP,
    CLASSES_TO_WRAP,
    RENDERED_JSON_FOLDER,
)
from legacy.extensions import (
    wrap_hanging_punctuation,
    typograph_html,
    hyphenate_html,
    highlight_precode,
)

from legacy.functions import RENDER_FUNCTIONS


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

    for related_page_slug in related_page_slugs:
        print(f'  Processing related page “{related_page_slug}”')
        with open(f'{RENDERED_JSON_FOLDER}/{related_page_slug}.json') as file:
            related_page_link = f'/{related_page_slug}' if related_page_slug != 'index' else '/'
            json_data[related_page_link] = json.load(file)[related_page_link]
    rendered_json_content = json.dumps(json_data)

    return rendered_html_content, rendered_json_content
