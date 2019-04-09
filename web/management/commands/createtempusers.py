import os
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'loads analytics data into database'

    def handle(self, *args, **options):
        # Create dictionary data
        groups = [
            {
                'name': 'CHIEF EXECUTIVES',
            },
            {
                'name': 'FINANCE DEPARTMENT',
            },
            {
                'name': 'CUSTOMER SERVICE DEPARTMENT',
            },
        ]
        users = [
            {
                'username': 'alice',
                'first_name': 'Alice',
                'last_name': 'Wonderland',
                'password': make_password('ab8401!!'),
                'email': 'alice.wonderland@shine.com.sg',
                'is_staff': True,
                'is_active': True,
            },
            {
                'username': 'bob',
                'first_name': 'Bob',
                'last_name': 'Builder',
                'password': make_password('ab8401!!'),
                'email': 'bob.builder@shine.com.sg',
                'is_staff': True,
                'is_active': True,
            },
            {
                'username': 'charlie',
                'first_name': 'Charlie',
                'last_name': 'Factory',
                'password': make_password('ab8401!!'),
                'email': 'charlie.factory@shine.com.sg',
                'is_staff': True,
                'is_active': True,
            },
        ]

        # Create Group objects
        for group in groups:
            try:
                Group.objects.create(**group)
            except IntegrityError:
                # Handle output for violating UNIQUE constraint
                self.stdout.write(self.style.NOTICE("Group already exists: {}".format(group)))
            except:
                # Handle output for unknown errors
                self.stdout.write(self.style.NOTICE("An unknown error has occured: {}".format(group)))

        # Create User objects
        for user in users:
            try:
                u = User.objects.create(**user)
            except IntegrityError:
                # Handle output for violating UNIQUE constraint
                self.stdout.write(self.style.NOTICE("User already exists: {}".format(user)))
            except:
                # Handle output for unknown errors
                self.stdout.write(self.style.NOTICE("An unknown error has occured: {}".format(user)))

        # Output result
        self.stdout.write(self.style.SUCCESS("Temporary users and groups were successfully created. Remember to configure their respective group memberships via the admin site."))
