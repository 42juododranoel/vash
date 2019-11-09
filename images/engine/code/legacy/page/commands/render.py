import json

from legacy.constants import (
    RENDERED_JSON_FOLDER,
)
from legacy.extensions import (
    wrap_hanging_punctuation,
    hyphenate_html,
    highlight_precode,
)


def render(slug, page_meta, template_name, no_images=False):
    for related_page_slug in related_page_slugs:
        print(f'  Processing related page “{related_page_slug}”')
        with open(f'{RENDERED_JSON_FOLDER}/{related_page_slug}.json') as file:
            related_page_link = f'/{related_page_slug}' if related_page_slug != 'index' else '/'
            json_data[related_page_link] = json.load(file)[related_page_link]
    rendered_json_content = json.dumps(json_data)

    return rendered_html_content, rendered_json_content
