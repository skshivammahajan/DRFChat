from django.apps import AppConfig


class FeedsConfig(AppConfig):
    name = 'feeds'

    def ready(self):
        from feeds.signals import handlers
