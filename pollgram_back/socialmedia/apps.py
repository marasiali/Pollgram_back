from django.apps import AppConfig


class SocialmediaConfig(AppConfig):
    name = 'socialmedia'

    def ready(self):
        import socialmedia.signals