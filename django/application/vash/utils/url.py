from constance import config


def get_base_url():
    protocol = 'https' if config.IS_HTTPS_ENABLED else 'http'
    domain = config.SITE_DOMAIN
    return f'{protocol}://{domain}'
