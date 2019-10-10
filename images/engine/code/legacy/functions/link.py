def link(slug, related_page_slugs):
    related_page_slugs.append(slug)
    return f'/{slug}' if slug != 'index' else '/'
