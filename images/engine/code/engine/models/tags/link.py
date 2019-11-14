from engine.utilities.path_to_link import path_to_link


def link(path, context):
    relations_set = set(context['forward-relations'])
    relations_set.add(path)
    relations_list = list(relations_set)
    context['forward-relations'] = relations_list
    return path_to_link(path)
