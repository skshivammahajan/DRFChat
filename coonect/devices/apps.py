from django.apps import AppConfig


class DevicesConfig(AppConfig):
    name = 'devices'

    def ready(self):
        import devices.signals.handlers
