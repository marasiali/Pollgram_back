from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Create site entry using "SITE_DOMAIN_NAME", "SITE_DISPLAY_NAME" parameters in settings'

    def handle(self, *args, **options):
        if Site.objects.count() == 0:
            Site.objects.create(domain=settings.SITE_DOMAIN_NAME, name=settings.SITE_DISPLAY_NAME)
            self.stdout.write(self.style.SUCCESS(f'Site entry for {settings.SITE_DISPLAY_NAME} created successfully. '))
        elif Site.objects.count() == 1 and Site.objects.filter(name='example.com').exists():
            obj = Site.objects.get(name='example.com')
            obj.domain = settings.SITE_DOMAIN_NAME
            obj.name = settings.SITE_DISPLAY_NAME
            obj.save()
            self.stdout.write(self.style.SUCCESS(f'Example site entry updated to {settings.SITE_DISPLAY_NAME} successfully. '))
        else:
            self.stdout.write(self.style.SUCCESS('Site entry exists! Nothing to do.'))