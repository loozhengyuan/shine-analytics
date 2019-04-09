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

        for user, group in zip(users, groups):
            # Group Object
            try:
                g = Group.objects.get(name=group['name'])
            except Group.DoesNotExist:
                self.stdout.write(self.style.NOTICE("{} does not exist. Creating Group object.".format(group)))
                g = Group.objects.create(**group)
            
            # User Object
            try:
                u = User.objects.get(username=user['username'])
            except User.DoesNotExist:
                self.stdout.write(self.style.NOTICE("{} does not exist. Creating User object.".format(user)))
                u = User.objects.create(**user)

            # Add Group to User
            try:
                u.groups.add(g)
            except:
                self.stdout.write(self.style.NOTICE("Could not associate user with group: {} {}".format(user, group)))

        # Output result
        self.stdout.write(self.style.SUCCESS("Temporary users and groups were successfully created."))
