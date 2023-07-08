# Michael Cassidy, 009986687

from HashMap import HashMap
from TextColor import TextColor
from Package import Package
import csv


def display_package_list(package_list):
    if len(package_list) > 0:
        extracted_attribute_list = []
        if isinstance(package_list[0], Package):
            for package in package_list:
                extracted_attribute_list.append(package.get_data())
        else:
            extracted_attribute_list = package_list
        headers = ["Status", "Status Updated", "ID", "Address", "City", "State", "Zip Code", "Deadline",
                   "Weight"]

        # Determine the maximum width for each column
        column_widths = [max(len(str(row[i])) for row in extracted_attribute_list
                             + [headers]) for i in range(len(headers))]

        # Print the headers
        header_line = " | ".join("{:{}}".format(header, column_widths[i]) for i, header in enumerate(headers))
        print('\n' + header_line)
        print("-" * len(header_line))

        for row in extracted_attribute_list:
            value = row[0]
            data_line = " | ".join("{:{}}".format(str(value), column_widths[i]) for i, value in enumerate(row))

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


def create_package_list():
    h = HashMap()
    with open('csv/WGUPS_Package_File.csv') as package_file:
        csv_reader = csv.reader(package_file)
        for line in csv_reader:
            notes = line[7]
            if 'delayed' in notes.lower():
                status = 'En route to Hub'
            elif 'wrong address' in notes.lower():
                status = 'Hold for correct address'
            else:
                status = 'At Hub'

            h.add(int(line[0]), Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], notes, status))
    return h
