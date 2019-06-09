from django.template.defaulttags import register


@register.filter
def get(mapping, key):
    return mapping.get(key) or ''
