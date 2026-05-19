from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a PetCad admin account (Django User with staff access).'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Admin email (used as username)')
        parser.add_argument('password', type=str, help='Admin password')
        parser.add_argument(
            '--name',
            type=str,
            default='',
            help='Display name (first name)',
        )

    def handle(self, *args, **options):
        email = options['email'].strip().lower()
        password = options['password']
        name = options['name'].strip()

        if User.objects.filter(username=email).exists():
            raise CommandError(f'An account with email "{email}" already exists.')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS(f'Admin created: {email}'))
        self.stdout.write('Log in at / with this email and password.')
