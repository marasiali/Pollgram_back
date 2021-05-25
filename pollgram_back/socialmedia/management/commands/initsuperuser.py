from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Create superuser if not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = settings.DEFAULT_SUPERUSER.get("USERNAME")
            password = settings.DEFAULT_SUPERUSER.get("PASSWORD")
            email = settings.DEFAULT_SUPERUSER.get("EMAIL")
            self.stdout.write(f'Create "{username}" superuser ...')
            user = User.objects.create_superuser(username=username, password=password, email=email)
            EmailAddress.objects.create(user=user, email=email, verified=True, primary=False)
            self.stdout.write(self.style.SUCCESS(f'"{username}" superuser was created successfully. '))
        else:
            self.stdout.write('The superuser exists. Nothing to do.')