import os
import csv
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'cleans data according to import conditions'

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
        omitted = []
        sanitised = []

        # Open file and append each entry in CSV file to the report list
        with open(filepath, "r") as f:
            data = csv.reader(f)
            for entry in data:
                original.append(entry)

        # Removes trailing whitespaces in all data
        original = [[data.strip() for data in entry] for entry in original]

        # Appends header to the two outputs lists
        omitted.append(original[0])
        sanitised.append(original[0])

        # Add reasons column specially for omitted list
        omitted[0].append('FailedConditions')
        
        # Loops through every line in dataset; omits header row
        for entry in original[1:]:
            # Initial Check: Exits function immediately if length of data entry incorrect
            if len(entry) != 14:
                raise CommandError("Size of data entry is invalid!")
            else:
                discard = False
                reasons = []

            # Omission 1: Omits if DocDate does not begin from 2016 onwards
            if int(entry[0][0:4]) < 2016:
                discard = True
                reasons.append("DocDate does not begin from 2016 onwards")

            # Omission 2: Omits if DocRef does not begin with B or I
            if entry[1][0].upper() not in ['B', 'I']:
                discard = True
                reasons.append("DocRef does not begin with B or I")
            
            # Omission 3: Omits if transaction in SGD but HomeWTaxAmt differs from AcCurWTaxAmt
            if entry[6].upper() == 'SGD' and abs(float(entry[7])) != abs(float(entry[8])):
                discard = True
                reasons.append("Transaction in SGD but HomeWTaxAmt differs from AcCurWTaxAmt")

            # Omission 4: Omits if transaction in USD but AcCurWTaxAmt is more than or equals to HomeWTaxAmt
            if entry[6].upper() == 'USD' and abs(float(entry[7])) >= abs(float(entry[8])):
                discard = True
                reasons.append("Transaction in USD but AcCurWTaxAmt is more than or equals to HomeWTaxAmt")

            # Omission 5: Omits if either AcCurWTaxAmt or HomeWTaxAmt is 0
            if float(entry[7]) == 0 or float(entry[8]) == 0:
                discard = True
                reasons.append("Either AcCurWTaxAmt or HomeWTaxAmt is 0")

            # Apply corrections and export if not omitted
            if not discard:
                # Correction 1: Apply abs() to all amounts
                entry[7] = abs(float(entry[7]))
                entry[8] = abs(float(entry[8]))

                # Correction 2: Apply -1 to B-prefix documents
                if entry[1][0].upper() == 'B':
                    entry[7] *= -1
                    entry[8] *= -1

                # Appends entry to sanitised list
                sanitised.append(entry)

            # Appends to omitted list if fails check
            else:
                # Appends reasons
                entry.append(", ".join(reasons))
                # Appends entry to omitted list
                omitted.append(entry)

        # Outputs sanitised list to sanitised.csv
        sanitised_filename = "sanitised.csv"
        with open(sanitised_filename, "w+") as f:
            pointer = csv.writer(f)
            pointer.writerows(sanitised)

        # Outputs omitted list to omitted.csv
        omitted_filename = "omitted.csv"
        with open(omitted_filename, "w+") as f:
            pointer = csv.writer(f)
            pointer.writerows(omitted)

        # Output result
        self.stdout.write(self.style.SUCCESS("{} entries were cleaned and exported to {}".format(len(sanitised[1:]), sanitised_filename)))
        self.stdout.write(self.style.SUCCESS("{} entries were omitted and exported to {}".format(len(omitted[1:]), omitted_filename)))
