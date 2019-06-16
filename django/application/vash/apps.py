from django.apps import AppConfig


class VashConfig(AppConfig):
    name = 'vash'

    def ready(self):
        import vash.signals
