from constance import config
from django.conf import settings


def get_base_url():
    protocol = 'https' if config.IS_HTTPS_ENABLED else 'http'
    domain = config.SITE_DOMAIN
    return f'{protocol}://{domain}'


def media_path_to_url(path):
    return path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL[:-1], 1)
