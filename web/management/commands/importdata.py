import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_date
from web.models import *

class Command(BaseCommand):
    help = 'loads analytics data into database'

    def add_arguments(self, parser):
        # Positional Arguments
        parser.add_argument('filepath', nargs='+', type=str)

    def handle(self, *args, **options):
        # Check if file exists in path
        filepath = options['filepath'][0]
        if not os.path.isfile(filepath):
            raise CommandError("{} does not exists!".format(filepath))

        # Creates a blank list for manipulating the data
        original = []

        # Open file and append each entry in CSV file to the report list
        with open(filepath, "r") as f:
            data = csv.reader(f)
            for entry in data:
                original.append(entry)

        # Removes trailing whitespaces in all data
        original = [[data.strip() for data in entry] for entry in original]

        # Declare counter variables
        imported = 0
        
        # Loops through every line in dataset; omits header row
        for entry in original[1:]:
            # Initial Check: Exits function immediately if length of data entry incorrect
            if len(entry) != 14:
                raise CommandError("Size of data entry is invalid!")
            else:
                try:
                    # Get or create Customer object
                    customer, created = Customer.objects.get_or_create(
                        name=entry[3],
                    )

                    # Get or create Currency object
                    currency, created = Currency.objects.get_or_create(
                        code=entry[6],
                    )

                    # Get or create CustomerAccount object
                    custaccount, created = CustomerAccount.objects.get_or_create(
                        code=entry[2],
                        postal=entry[4],
                        contact=entry[5],
                        customer=customer,
                        currency=currency,
                    )

                    # Get or create SalesPerson object
                    salesperson, created = SalesPerson.objects.get_or_create(
                        code=entry[11],
                        name=entry[12],
                        contact=entry[13],
                    )
                    
                    # Get or create Project object
                    project, created = Project.objects.get_or_create(
                        code=entry[9],
                        custaccount=custaccount,
                        salesperson=salesperson,
                    )

                    # Get or create Document object
                    document, created = Document.objects.get_or_create(
                        date=parse_date("{}-{}-{}".format(entry[0][0:4], entry[0][4:6], entry[0][6:8])),
                        reference=entry[1],
                    )

                    # Get or create Location object
                    location, created = Location.objects.get_or_create(
                        code=entry[10],
                    )

                    # Create Transaction object
                    transaction = Transaction.objects.create(
                        document=document,
                        project=project,
                        location=location,
                        transacted_amount=entry[7],
                        converted_amount=entry[8],
                    )

                    # Increment counter
                    imported += 1

                except IntegrityError:
                    # Handle output for violating UNIQUE constraint
                    self.stdout.write(self.style.NOTICE("Document already exists: {}".format(entry)))
                except:
                    # Handle output for unknown errors
                    self.stdout.write(self.style.NOTICE("An unknown error has occured: {}".format(entry)))

        # Output result
        self.stdout.write(self.style.SUCCESS("{}/{} entries were imported into the database".format(imported, len(original[1:]))))
