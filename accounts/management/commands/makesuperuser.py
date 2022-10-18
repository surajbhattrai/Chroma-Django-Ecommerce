from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(phone="9876543210").exists():
            User.objects.create_superuser(first_name="Suraj",last_name="Bhattarai",phone="9876543210", email="admin@gmail.com", password="admin")
            self.stdout.write(self.style.SUCCESS('Successfully created superuser!'))
        else:
            self.stdout.write(self.style.NOTICE('Superuser already exists.'))

