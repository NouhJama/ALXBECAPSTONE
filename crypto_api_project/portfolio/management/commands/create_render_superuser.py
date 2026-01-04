from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser for Render deployment'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv('RENDER_SUPERUSER_USERNAME')
        email = os.getenv('RENDER_SUPERUSER_EMAIL')
        password = os.getenv('RENDER_SUPERUSER_PASSWORD')

        if not email or not password:
            self.stdout.write(self.style.ERROR(
                'RENDER_SUPERUSER_EMAIL and RENDER_SUPERUSER_PASSWORD environment are missing.'
            ))
            return
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Superuser with username "{username}" already exists.'
            ))
            return
        
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
