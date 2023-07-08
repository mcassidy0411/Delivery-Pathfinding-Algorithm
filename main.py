# Michael Cassidy, 009986687

import copy
import time
import PackageHandler
import TimeUtils
from TextColor import TextColor
from HashMap import HashMap
from Truck import Truck


class Main:
    def run_delivery_simulation(package_list, stop_time=None):
        def load_truck(truck, packages):
            for i in packages:
                package = package_list.get(i)
                package.status = f'On Truck {truck.truck_number} for delivery'
                package.last_modified = truck.master_time
                original_package_list.append(package.get_data())
                truck.add(package)

        def deliver(truck):
            for i in range(truck.count):
                original_package_list.append(truck.deliver_next().get_data())
            truck.deliver_next()

        def print_truck_status(truck):
            if no_stop_time:
                print(TextColor.bright_blue + f'\nTruck {truck.truck_number} left the Hub at {truck.next_departure_time}.'
                      f' Trip Number: {truck.trip_number}' + TextColor.reset)
                time.sleep(0.5)
                PackageHandler.display_package_list(truck.delivered_package_list)
                print(TextColor.bright_blue + f'\nTruck {truck.truck_number} returned to the Hub at {truck.master_time}'
                      + TextColor.reset)

        stop_time = TimeUtils.parse_time_string(stop_time)
        no_stop_time = False
        if stop_time is None:
            no_stop_time = True

        original_package_list = []

        for i in range(1, package_list.number_of_items + 1):
            package = package_list.get(i)
            original_package_list.append(copy.copy(package.get_data()))

        truck1 = Truck(1, '08:00')
        truck2 = Truck(2, '08:00')

        # Load Trucks
        truck1_packages = [1, 2, 4, 13, 14, 15, 16, 19, 20, 21, 27, 33, 34, 35, 39, 40]
        truck2_packages = [3, 5, 7, 8, 10, 11, 17, 18, 22, 23, 24, 29, 30, 36, 37, 38]

        load_truck(truck1, truck1_packages)
        load_truck(truck2, truck2_packages)

        deliver(truck1)
        deliver(truck2)
        print_truck_status(truck1)
        print_truck_status(truck2)

        delayed_packages = [6, 25, 28, 32]
        for i in delayed_packages:
            package = package_list.get(i)
            package.status = 'At Hub'
            package.last_modified = TimeUtils.parse_time_string('09:05')
            original_package_list.append(package.get_data())
            if no_stop_time:
                print(TextColor.bright_yellow + f'\nAt 9:05, Package {package.package_id} arrived at the Hub' + TextColor.reset)

        truck1_packages = [6, 25, 26, 31, 32]
        load_truck(truck1, truck1_packages)
        deliver(truck1)

        package9 = package_list.get(9)
        package9.address = '410 S State St'
        package9.city = 'Salt Lake City'
        package9.state = 'UT'
        package9.zip_code = '84111'
        package9.notes = 'Address Corrected'
        package9.status = 'At Hub'
        package9.last_modified = TimeUtils.parse_time_string('10:20')
        original_package_list.append(package9.get_data())

        truck2_packages = [9, 12, 28]
        load_truck(truck2, truck2_packages)
        if truck2.master_time < TimeUtils.parse_time_string('10:20'):
            if no_stop_time:
                print(TextColor.red + '\nTruck 2 Holding until 10:20 for correct address on Package 9'
                      + TextColor.reset)
            truck2.master_time = TimeUtils.parse_time_string('10:20')
            truck2.next_departure_time = truck2.master_time

        if no_stop_time:
            print(TextColor.bright_yellow + "\nAt 10:20, Package 9's address was corrected." + TextColor.reset)

        deliver(truck2)

        print_truck_status(truck1)
        print_truck_status(truck2)

        unique_entries = []
        if no_stop_time:
            truck1_total_time = truck1.master_time - TimeUtils.parse_time_string("08:00")
            truck2_total_time = truck2.master_time - TimeUtils.parse_time_string("08:00")

            print(TextColor.bright_green + '\nSummary\n--------------------------------------------' + TextColor.reset)
            print(f'Truck 1 total mileage: {round(truck1.mileage, 2)}\nTruck 1 total time: {truck1_total_time}')
            print(f'Truck 2 total mileage: {round(truck2.mileage, 2)}\nTruck 2 total time: {truck2_total_time}')
            print(f'Total Mileage Travelled by all Trucks: {round(truck1.mileage + truck2.mileage)}')
            print(f'Total Delivery Time for all Trucks: {truck1_total_time + truck2_total_time}')
            print(TextColor.bright_green + '--------------------------------------------' + TextColor.reset)
        else:
            seen_keys = set()
            for entry in reversed(original_package_list):
                if entry[1] > stop_time:
                    original_package_list.remove(entry)
                else:
                    key = entry[2]
                    if key not in seen_keys:
                        unique_entries.append(entry)
                        seen_keys.add(key)

        unique_entries.sort()
        return unique_entries

    while True:
        package_hash_table = PackageHandler.create_package_list()

        prompt = TextColor.blue + '\nWhat would you like to do?\n' + TextColor.reset + \
                                            '\n1. Begin delivery simulation' \
                                            '\n2. Lookup Package' \
                                            '\n3. Quit\n\n>> '
        try:
            user_input = int(input(prompt))
        except ValueError:
            print(TextColor.red + 'Please enter a valid option' + TextColor.reset)
            continue
        if user_input == 1:
            run_delivery_simulation(package_hash_table)
        elif user_input == 2:

            while True:
                lookup_time_prompt = TextColor.blue + '\nEnter a time in 24 hour format ("HH:MM") to check the ' \
                                                            'status of deliveries: (For example, "13:15" for 1:15 PM)\n' \
                                                            + TextColor.reset + '\n>> '
                try:
                    lookup_time = input(lookup_time_prompt)
                    package_list = run_delivery_simulation(package_hash_table, lookup_time)
                except ValueError:
                    print(TextColor.red + '\nPlease enter a valid time' + TextColor.reset)
                    continue

                while True:
                    lookup_prompt_list = [[1, 'All Packages'], [2, 'Package ID'], [3, 'Address'], [4, 'City'],
                                          [5, 'Zip Code'], [6, 'Package Weight'], [7, 'Delivery Deadline'], [8, 'Status'],
                                          [9, 'Back to Main Menu']]

                    lookup_prompt_hashmap = HashMap()
                    for i in range(len(lookup_prompt_list)):
                        row = lookup_prompt_list[i]
                        lookup_prompt_hashmap.add(row[0], row[1])

                    lookup_filter_prompt = TextColor.blue + '\nWhat would you like to look up?\n' \
                                            + TextColor.reset

                    print(lookup_filter_prompt)
                    for i in range(1, lookup_prompt_hashmap.number_of_items + 1):
                        print(f'{i}. {lookup_prompt_hashmap.get(i)}')

                    try:
                        lookup_selection = int(input('\n>> '))
                    except ValueError:
                        print(TextColor.red + 'Please enter a valid option' + TextColor.reset)
                        continue

                    lookup_value = None
                    return_to_main_menu = False
                    if lookup_prompt_hashmap.get(lookup_selection) is None:
                        print(TextColor.red + 'Please make a valid selection' + TextColor.reset)
                        continue
                    elif 2 <= lookup_selection <= 7:
                        lookup_value = input(TextColor.blue +
                                             f'\nPlease enter the {lookup_prompt_hashmap.get(lookup_selection)}:\n'
                                             + TextColor.reset + '\n>> ').lower()
                    elif lookup_selection == 8:
                        while True:
                            try:
                                status_selection = int(input(TextColor.blue + '\nPlease select a status:' + TextColor.reset
                                                         + '\n\n1. Delivered\n2. Out For Delivery\n3. At Hub'
                                                           '\n4. En Route to Hub\n5. Hold\n\n>> '))
                                if status_selection == 1:
                                    lookup_value = 'delivered'
                                elif status_selection == 2:
                                    lookup_value = 'out for delivery'
                                elif status_selection == 3:
                                    lookup_value = 'at hub'
                                elif status_selection == 4:
                                    lookup_value = 'en route to hub'
                                elif status_selection == 5:
                                    lookup_value = 'hold'
                                break
                            except ValueError:
                                print(TextColor.red + 'Please select a valid option' + TextColor.reset)
                                continue
                    elif lookup_selection == 9:
                        return_to_main_menu = True
                        break

                    filtered_list = []
                    for package in package_list:
                        current_package = package
                        if lookup_selection == 1:
                            filtered_list[:] = package_list
                            break
                        elif lookup_selection == 2:
                            if current_package[2] == int(lookup_value):
                                filtered_list.append(current_package)
                                break
                        elif lookup_selection == 3:
                            if current_package[3].lower() == lookup_value:
                                filtered_list.append(current_package)
                        elif lookup_selection == 4:
                            if current_package[4].lower() == lookup_value:
                                filtered_list.append(current_package)
                        elif lookup_selection == 5:
                            if current_package[6] == lookup_value:
                                filtered_list.append(current_package)
                        elif lookup_selection == 6:
                            if current_package[8] == lookup_value:
                                filtered_list.append(current_package)
                        elif lookup_selection == 7:
                            if lookup_value in current_package[7].lower():
                                filtered_list.append(current_package)
                        elif lookup_selection == 8:
                            if lookup_value in current_package[0].lower():
                                filtered_list.append(current_package)

                    PackageHandler.display_package_list(filtered_list)

                if return_to_main_menu:
                    break

        elif user_input == 3:
            print('Quitting')
            break
        else:
            print(TextColor.red + 'Please enter a valid option' + TextColor.reset)
