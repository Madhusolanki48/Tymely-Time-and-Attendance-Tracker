from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Deploy the application - run migrations and collect static files'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting deployment process...'))
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate', '--noinput')
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput')
        
        self.stdout.write(self.style.SUCCESS('Deployment completed successfully!'))
