def path_to_link(path):
    if path == 'index':
        link = '/'
    else:
        link = f'/{path}'
    return link
