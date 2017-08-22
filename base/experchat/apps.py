from django.apps import AppConfig


class ExperchatConfig(AppConfig):
    name = 'experchat'

    def ready(self):
        from experchat import signals
