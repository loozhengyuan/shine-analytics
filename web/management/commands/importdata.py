import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_date
from ...models import AccountsReceivable

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
                # Create AccountsReceivable object
                try:
                    a = AccountsReceivable(
                            docdate = parse_date("{}-{}-{}".format(entry[0][0:4], entry[0][4:6], entry[0][6:8])),
                            docref = entry[1],
                            actcode = entry[2],
                            cusname = entry[3],
                            postcode = entry[4],
                            custel = entry[5],
                            actcur = entry[6],
                            actcurwtax = entry[7],
                            homecurwtax = entry[8],
                            projcode = entry[9],
                            location = entry[10],
                            salescode = entry[11],
                            salesname = entry[12],
                            salestel = entry[13],
                        )
                    
                    # Save and commit entry
                    a.save()

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
