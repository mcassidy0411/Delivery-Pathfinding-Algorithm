import datetime
import csv
from abc import ABC, abstractmethod
from TextColor import TextColor


class HashMap:
    def __init__(self):
        self.size = 8
        self.map = [None] * self.size
        self.number_of_items = 0

    def get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]
        self.number_of_items += 1
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for item in self.map[key_hash]:
                if item[0] == key:
                    item[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for item in self.map[key_hash]:
                if item[0] == key:
                    return item[1]
        return None

    def delete(self, key):
        key_hash = self.get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def display(self):
        for item in self.map:
            if item is not None:
                print(str(item))


class AdjacencyMatrix:
    def __init__(self):
        self.address_dict = {}
        self.adjacency_dict = {}
        with open('csv/WGUPS_Distance_Table.csv') as distance_file:
            csv_reader = csv.reader(distance_file)
            self.adjacency_matrix = [line for line in csv_reader]

            for i in range(len(self.adjacency_matrix)):
                # Puts address in the correct format and moves to indices list.
                # This list will look up index by address and vice versa
                row = self.adjacency_matrix[i]
                address = str(row.pop(0))
                new_address = address.split('\n', 1)[-1].split(',', 1)[0].strip()

                iterator = 1
                for j in range(len(self.adjacency_matrix)):
                    if row[j] == '':
                        row[j] = self.adjacency_matrix[i + iterator][j - iterator + 1]
                        iterator += 1
                    row[j] = float(row[j])
                self.address_dict[new_address] = i
                self.adjacency_dict[i] = row

    def get_distance_between(self, point_a, point_b):
        point_a_index = self.address_dict[point_a]
        point_b_index = self.address_dict[point_b]
        adjacency_list = self.adjacency_dict[point_a_index]
        return float(adjacency_list[point_b_index])


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def get_data(self):
        return [self.package_id, self.address, self.city, self.state, self.zip_code, self.deadline, self.weight,
                self.status]


class Truck:
    def __init__(self, truck_number, departure_time, stop_time=None):
        self.delivery_list = [None] * 16
        self.truck_number = truck_number
        self.count = 0
        self.mileage = 0.0
        self.hub = '4001 South 700 East'
        self.current_location = self.hub
        self.master_time = parse_time_string(departure_time)
        self.distance_table = AdjacencyMatrix()
        self.trip_number = 1
        self.stop_time = stop_time
        self.status = 'At Hub'
        self.delivered_package_list = []

    def add(self, package):
        if self.count < len(self.delivery_list):
            package.status = f'On Truck {self.truck_number} for delivery'
            self.delivery_list[self.count] = package
            self.count += 1
            return True
        return False

    def deliver(self):
        while True:
            if self.stop_time is None:
                print(f'\nTruck {self.truck_number}, Trip {self.trip_number} Delivering Packages:\n')
            while self.count > 0:

                current_package = self.delivery_list[0]
                shortest_distance = self.distance_table.get_distance_between(self.current_location,
                                                                             self.delivery_list[0].address)
                for j in range(self.count):
                    distance = self.distance_table.get_distance_between(self.current_location,
                                                                        self.delivery_list[j].address)
                    if distance <= shortest_distance:
                        shortest_distance = distance
                        current_package = self.delivery_list[j]

                self.current_location = current_package.address
                self.status = f'En Route to {self.current_location} at {self.master_time}'
                next_delivery_time = self.calculate_time(shortest_distance)

                if self.stop_time is not None and self.stop_time < next_delivery_time:
                    break

                self.set_time(shortest_distance)
                self.set_mileage(shortest_distance)
                current_package.status = f'Delivered at {self.master_time}'

                if self.stop_time is None:
                    self.delivered_package_list.append(current_package)

                self.delivery_list.pop(self.delivery_list.index(current_package))
                self.count -= 1

            if self.count == 0 and self.stop_time is not None:
                distance_to_hub = self.distance_table.get_distance_between(self.current_location, self.hub)
                if self.stop_time < self.calculate_time(distance_to_hub):
                    self.status = f'Returning to Hub at {self.master_time}'
                    break
                else:
                    self.return_to_hub()
            else:
                self.return_to_hub()

            break

    def calculate_time(self, distance):
        hours = distance / 18
        current_time = self.master_time
        current_time += datetime.timedelta(hours=hours)
        return current_time

    def set_time(self, distance):
        hours = distance / 18
        self.master_time += datetime.timedelta(hours=hours)

    def set_mileage(self, distance):
        self.mileage += distance

    def return_to_hub(self):
        distance_to_hub = self.distance_table.get_distance_between(self.current_location, self.hub)
        self.set_time(distance_to_hub)
        self.set_mileage(distance_to_hub)
        self.delivery_list = [None] * 16
        self.count = 0
        self.trip_number += 1
        self.status = f'Returned to Hub at {self.master_time}'
        display_package_list(self.delivered_package_list)
        self.delivered_package_list = []

    def print_delivery(self, current_package):
        data = [{'package_id': current_package.package_id, 'address': current_package.address,
                 'delivery_time': self.master_time}]
        for item in data:
            output = f"Package {item['package_id']:2} {item['address']:20} Delivered at {item['delivery_time']}"
            print(output)


def create_package_list():
    h = HashMap()
    with open('csv/WGUPS_Package_File.csv') as package_file:
        csv_reader = csv.reader(package_file)
        for line in csv_reader:
            notes = line[7]
            status = None
            if notes == '':
                notes = None
                status = 'At Hub'
            elif 'delayed' in notes.lower():
                status = 'En route to Hub'
            elif 'wrong address' in notes.lower():
                status = 'Holding for corrected address'

            h.add(int(line[0]), Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], notes, status))
    return h


def parse_time_string(time):
    try:
        hours, minutes = time.split(":")
        return datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
    except AttributeError:
        return None


def display_package_list(list):
    if len(list) > 0:
        extracted_attribute_list = []

        for package in list:
            extracted_attribute_list.append(package.get_data())

        headers = ["Package ID", "Address", "City", "State", "Zip Code", "Deadline", "Weight", "Status"]

        # Determine the maximum width for each column
        column_widths = [max(len(str(row[i])) for row in extracted_attribute_list + [headers]) for i in range(len(headers))]

        # Print the headers
        header_line = " | ".join("{:{}}".format(header, column_widths[i]) for i, header in enumerate(headers))
        print(TextColor.magenta + header_line)
        print("-" * len(header_line) + TextColor.reset)

        # Print the data rows
        for row in extracted_attribute_list:
            data_line = " | ".join("{:{}}".format(str(value), column_widths[i]) for i, value in enumerate(row))
            print(data_line)


def deliver_packages(package_list, stop_time=None):
    def load_truck(truck, packages):
        for i in packages:
            truck.add(package_list.get(i))

    stop_time = parse_time_string(stop_time)

    truck1 = Truck(1, '08:00', stop_time)
    truck2 = Truck(2, '08:00', stop_time)

    # Load Trucks
    truck1_packages = [1, 2, 4, 13, 14, 15, 16, 19, 20, 21, 27, 33, 34, 35, 39, 40]
    truck2_packages = [3, 5, 7, 8, 10, 11, 17, 18, 22, 23, 24, 29, 30, 36, 37, 38]

    load_truck(truck1, truck1_packages)
    load_truck(truck2, truck2_packages)

    truck1.deliver()
    display_package_list(truck1.delivered_package_list)
    truck2.deliver()
    display_package_list(truck2.delivered_package_list)

    if stop_time is None or stop_time >= datetime.datetime.now().replace(hour=9, minute=5, second=0, microsecond=0):
        delayed_packages = [6, 25, 28, 32]
        for i in delayed_packages:
            package_list.get(i).status = 'At Hub'

    if stop_time is None or stop_time >= datetime.datetime.now().replace(hour=10, minute=20, second=0, microsecond=0):
        package9 = package_list.get(9)
        package9.address = '410 S State St'
        package9.city = 'Salt Lake City'
        package9.state = 'UT'
        package9.zip_code = '84111'
        package9.notes = 'Address Corrected'
        package9.status = 'At Hub'

    if stop_time is None or (stop_time is not None and truck1.master_time < stop_time):
        truck1_packages = [6, 25, 26, 31, 32]
        load_truck(truck1, truck1_packages)
        truck1.deliver()
        display_package_list(truck1.delivered_package_list)

    if stop_time is None or (stop_time is not None and truck2.master_time < stop_time):
        truck2_packages = [9, 12, 28]
        load_truck(truck2, truck2_packages)
        # If Truck 2 returns to the Hub prior to 10:20, hold Truck 2 until Package 9's corrected address is received at
        # 10:20.  Begin next trip at 10:20
        if truck2.master_time < datetime.datetime.now().replace(hour=10, minute=20, second=0, microsecond=0):
            truck2.master_time = datetime.datetime.now().replace(hour=10, minute=20, second=0, microsecond=0)
        truck2.deliver()
        display_package_list(truck2.delivered_package_list)


while True:
    package_hash_table = create_package_list()

    prompt = TextColor.blue + '\nWhat would you like to do?\n' + TextColor.reset + \
                                        '\n1. Begin delivery simulation' \
                                        '\n2. Lookup Package' \
                                        '\n3. Quit\n\n>> '
    try:
        user_input = int(input(prompt))
    except ValueError:
        print('Please enter a valid option')
        continue
    if user_input == 1:
        deliver_packages(package_hash_table)
    elif user_input == 2:

        while True:
            lookup_time_prompt = TextColor.blue + '\nEnter a time in 24 hour format ("HH:MM") to check the ' \
                                                        'status of deliveries: (For example, "13:15" for 1:15 PM)\n' \
                                                        + TextColor.reset + '\n>> '
            try:
                lookup_time = input(lookup_time_prompt)
                deliver_packages(package_hash_table, lookup_time)
            except ValueError:
                print('Please enter a valid time')
                continue

            while True:
                lookup_prompt_dict = {1: 'All Packages',
                                      2: 'Package ID',
                                      3: 'Address',
                                      4: 'City',
                                      5: 'Zip Code',
                                      6: 'Package Weight',
                                      7: 'Delivery Deadline',
                                      8: 'Status',
                                      9: 'Back to Main Menu'}

                lookup_filter_prompt = TextColor.blue + '\nWhat would you like to look up?\n\n' \
                                        + TextColor.reset
                for key, value in lookup_prompt_dict.items():
                    lookup_filter_prompt += f'{str(key)}. {value}\n'
                lookup_filter_prompt += '\n>> '

                try:
                    lookup_selection = int(input(lookup_filter_prompt))
                except ValueError:
                    print('Please enter a valid option')
                    continue

                return_to_main_menu = False
                if lookup_prompt_dict.get(lookup_selection) is None:
                    print('Please make a valid selection')
                    continue
                elif 2 <= lookup_selection <= 8:
                    lookup_value = input(TextColor.blue +
                                         f'\nPlease enter the {lookup_prompt_dict.get(lookup_selection)}:\n'
                                         + TextColor.reset + '\n>> ').lower()
                elif lookup_selection == 9:
                    return_to_main_menu = True
                    break

                package_list = []
                filtered_list = []
                for i in range(1, package_hash_table.number_of_items + 1):
                    package_list.append(package_hash_table.get(i))

                for package in package_list:
                    current_package = package
                    if lookup_selection == 1:
                        lookup_value = None
                        filtered_list[:] = package_list
                        break
                    elif lookup_selection == 2:
                        if current_package.package_id == int(lookup_value):
                            filtered_list.append(current_package)
                            break
                    elif lookup_selection == 3:
                        if current_package.address.lower() == lookup_value:
                            filtered_list.append(current_package)
                    elif lookup_selection == 4:
                        if current_package.city.lower() == lookup_value:
                            filtered_list.append(current_package)
                    elif lookup_selection == 5:
                        if current_package.zip == lookup_value:
                            filtered_list.append(current_package)
                    elif lookup_selection == 6:
                        if current_package.weight == lookup_value:
                            filtered_list.append(current_package)
                    elif lookup_selection == 7:
                        if current_package.deadline == lookup_value:
                            filtered_list.append(current_package)
                    elif lookup_selection == 8:
                        if current_package.city == lookup_value:
                            filtered_list.append(current_package)

                display_package_list(filtered_list)

            if return_to_main_menu:
                break

    elif user_input == 3:
        print('Quitting')
        break
    else:
        print('Please enter a valid option')
