# Michael Cassidy, 009986687

from HashTable import HashTable
from TextColor import TextColor
from Package import Package
import csv


# Take a list of Package objects or a 2D list of Package attributes and displays in an organized, color-coded table on
# the console.  O(3n) -> O(n)
def display_package_list(package_list):

    # Checks if input list is empty
    if len(package_list) > 0:

        # Initializes empty list to hold package attributes
        extracted_attribute_list = []

        # Determines if package_list is a list of Package objects.
        if isinstance(package_list[0], Package):

            # If package_list is a list of Package objects, iterate through all Package objects, get Package attributes
            # and store in extracted_attribute_list O(n)
            for package in package_list:
                extracted_attribute_list.append(package.get_data())

        # If package_list was already a list of Package attributes, set extracted_attribute_list equal to package_list
        else:
            extracted_attribute_list = package_list

        # Set headers for table
        headers = ["Status", "Status Updated", "ID", "Address", "City", "State", "Zip Code", "Deadline",
                   "Weight"]

        # Determine the maximum width for each column based on max length of each data attribute. O(2n) -> O(n)
        column_widths = [max(len(str(row[i])) for row in extracted_attribute_list
                             + [headers]) for i in range(len(headers))]

        # Print the headers.  Note that in line 40, the function is using list comprehension, not a for loop.  O(1)
        header_line = " | ".join("{:{}}".format(header, column_widths[i]) for i, header in enumerate(headers))
        print('\n' + header_line)
        print("-" * len(header_line))

        # Iterate over all rows of extracted_attribute_list.  Note that in line 48, the function is using list
        # comprehension, not a for loop.  O(n)
        for row in extracted_attribute_list:

            # Set value to what the 0 index of the row, package status
            value = row[0]

            # Set line to be printed using list comprehension
            data_line = " | ".join("{:{}}".format(str(value), column_widths[i]) for i, value in enumerate(row))

            # Set the color of the line by status and print to console
            if 'delivered' in value.lower():
                print(TextColor.green + data_line + TextColor.reset)
            elif 'on truck' in value.lower():
                print(TextColor.bright_yellow + data_line + TextColor.reset)
            elif 'at hub' in value.lower():
                print(TextColor.cyan + data_line + TextColor.reset)
            elif 'en route to hub' in value.lower():
                print(TextColor.red + data_line + TextColor.reset)
            elif 'hold' in value.lower():
                print(TextColor.bright_magenta + data_line + TextColor.reset)


# Creates Package HashTable from data in 'csv/WGUPS_Package_File.csv'.  Iterates over each row of the file.  O(n)
def create_package_list():
    # Initialize a new, empty HashTable
    h = HashTable()

    with open('csv/WGUPS_Package_File.csv') as package_file:
        csv_reader = csv.reader(package_file)

        # For each line in file
        for line in csv_reader:

            # Set column index 7 to notes
            notes = line[7]

            # Check if conditions in notes exist and set status variable accordingly
            if 'delayed' in notes.lower():
                status = 'En route to Hub'
            elif 'wrong address' in notes.lower():
                status = 'Hold for correct address'
            else:
                status = 'At Hub'

            # Adds [package_id, Package Object] key-value pair to HashTable
            h.add(int(line[0]), Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], notes, status))
    return h
