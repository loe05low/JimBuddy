from django.core.management.base import BaseCommand
from achievements.utils import create_default_achievements


class Command(BaseCommand):
    help = 'Creates default achievements in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating default achievements...'))
        created_count = create_default_achievements()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} achievements!')
        )
