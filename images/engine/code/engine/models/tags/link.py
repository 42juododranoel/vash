from engine.utilities.path_to_link import path_to_link


def link(path, context):
    context['relations-from-me'].append(path)
    return path_to_link(path)
