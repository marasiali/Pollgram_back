from django.apps import AppConfig


class NotificationSystemConfig(AppConfig):
    name = 'notification_system'

    def ready(self):
        import notification_system.signals