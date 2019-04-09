import os
import csv
import string
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
        
        # Appends header to the two outputs lists
        omitted.append(original[0])
        sanitised.append(original[0])

        # Remove header row
        original.pop(0)

        # Add reasons column specially for omitted list
        omitted[0].append('FailedConditions')

        # Correction 1: Removes trailing whitespaces in all data
        original = [[data.strip() for data in entry] for entry in original]

        # Correction 2: Removes non-alphanumeric characters in DocRef & AcCode
        original = [[data.translate(str.maketrans('', '', string.punctuation + string.whitespace)) if index in [
            1, 2] else data for index, data in enumerate(entry)] for entry in original]

        # Correction 3: Apply abs() to AcCurWTaxAmt or HomeWTaxAmt
        original = [[abs(float(data)) if index in [
            7, 8] else data for index, data in enumerate(entry)] for entry in original]

        # Correction 4: Apply correct polarity to AcCurWTaxAmt or HomeWTaxAmt
        original = [[data * -1 if index in [7, 8] and entry[1][0].upper() ==
                     'B' else data for index, data in enumerate(entry)] for entry in original]

        # Loops through every line in dataset; omits header row
        for entry in original:
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

            # Appends entry to sanitised list
            if not discard:
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
