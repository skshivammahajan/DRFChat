from django.apps import AppConfig


class SessionsConfig(AppConfig):
    name = 'experchat_sessions'

    def ready(self):
        import experchat_sessions.signals.handlers
