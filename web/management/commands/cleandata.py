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
                outcome = True
                reasons = []

            # Condition 1: Checks if DocDate begins from 2016 onwards
            if int(entry[0][0:4]) < 2016:
                outcome = False
                reasons.append("Condition 1: DocDate does not begin from 2016 onwards")

            # Condition 2: Checks if DocRef begins with B or I, case insensitive
            if entry[1][0].upper() not in ['B', 'I']:
                outcome = False
                reasons.append("Condition 2: DocRef does not begin with B or I")

            # Condition 3: Checks if AcCur is USD or SGD
            if entry[6].upper() not in ['USD', 'SGD']:
                outcome = False
                reasons.append("Condition 3: AcCur is not USD or SGD")
            
            # Condition 4: Checks if AcCurWTaxAmt and HomeWTaxAmt is same if transaction in SGD
            if entry[6].upper() == 'SGD' and float(entry[7]) != float(entry[8]):
                outcome = False
                reasons.append("Condition 4: HomeWTaxAmt is not the same as AcCurWTaxAmt when AcCur is SGD")

            # Condition 5: Checks if polarity of AcCurWTaxAmt and HomeWTaxAmt is identical
            if (float(entry[7]) < 0 and float(entry[8]) > 0) or (float(entry[7]) > 0 and float(entry[8]) < 0):
                outcome = False
                reasons.append("Condition 5: Polarity of AcCurWTaxAmt and HomeWTaxAmt is different")

            # Condition 6: Checks if AcCurWTaxAmt and HomeWTaxAmt is 0 when either of them are
            if (float(entry[7]) == 0 and float(entry[8]) != 0) or (float(entry[7]) != 0 and float(entry[8]) == 0):
                outcome = False
                reasons.append("Condition 6: AcCurWTaxAmt and HomeWTaxAmt should be 0 if either are")

            # Condition 7: Checks if Location is within 1, 2, 3, 4, 5
            if int(entry[10]) not in [1, 2, 3, 4, 5]:
                outcome = False
                reasons.append("Condition 7: Location code not within range of 1-5")

            # Appends to sanitised list if passes check
            if outcome:
                # Appends entry to sanitised list
                sanitised.append(entry)

            # Appends to omitted list if fails check
            else:
                # Appends reasons
                entry.append("\n".join(reasons))
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
