from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Set up the application for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up production environment...'))

        # Run migrations
        self.stdout.write('Running database migrations...')
        call_command('migrate', verbosity=0)
        self.stdout.write(self.style.SUCCESS('✓ Database migrations completed'))

        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=0)
        self.stdout.write(self.style.SUCCESS('✓ Static files collected'))

        # Create superuser if requested
        if options['create_superuser']:
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write('Creating superuser...')
                username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
                email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
                password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
                
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Superuser "{username}" created'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists'))

        self.stdout.write(self.style.SUCCESS('Production setup completed successfully!'))
