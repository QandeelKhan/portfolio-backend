from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand

class Command(createsuperuser.Command):
    help = 'Create a new superuser'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Welcome to the Superuser Creation Wizard of QandeelKhan.com!'))
        self.stdout.write(self.style.WARNING('Please follow the prompts to create a new superuser.\n'))

        super().handle(*args, **options)
