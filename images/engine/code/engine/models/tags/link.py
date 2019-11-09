def link(slug, context):
    context['relations-from-me'].append(slug)

    if slug == 'index':
        link = '/'
    else:
        link = f'/{slug}'

    return link
