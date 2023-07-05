import datetime
import csv


class HashMap:
    def __init__(self):
        self.size = 8
        self.map = [None] * self.size

    def get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]

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


class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, weight, notes):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At Hub"

    def display(self):
        print(f'{self.package_id}, {self.address}, {self.city}, {self.state}, {self.zip}, '
              f'{self.deadline}, {self.weight}, {self.notes}, {self.status}')


class AdjacencyMatrix:
    def __init__(self):
        with open('csv/WGUPS_Distance_Table.csv') as distance_file:
            csv_reader = csv.reader(distance_file)
            self.adjacency_matrix = [line for line in csv_reader]
            self.indices = [None, None] * len(self.adjacency_matrix)

            for i in range(len(self.adjacency_matrix)):
                # Puts address in the correct format and moves to indices list.
                # This list will look up index by address and vice versa
                row = self.adjacency_matrix[i]
                address = str(row.pop(0))
                new_address = address.split('\n', 1)[-1].split(',', 1)[0].strip()
                self.indices[i] = new_address

                iterator = 1
                for j in range(len(self.adjacency_matrix)):
                    if self.adjacency_matrix[i][j] == '':
                        self.adjacency_matrix[i][j] = self.adjacency_matrix[i + iterator][j - iterator + 1]
                        iterator += 1
            # for i in range(len(self.adjacency_matrix)):
            #     print(type(self.adjacency_matrix[i]))

    def get_adjacency_list(self, address):
        for i in range(len(self.indices)):
            if address == self.indices[i]:
                return self.adjacency_matrix[i]

    def get_distance_between(self, point_a, point_b):
        list = self.get_adjacency_list(point_a)
        index = self.get_address_index(point_b)
        # print(index)
        # print(f'Point A: {point_a}\nPoint B: {point_b}\nDistance: {list[index]}')
        return float(list[index])

    def get_address_index(self, address):
        return self.indices.index(address)

    def get_next_closest(self, address):
        index = self.get_address_index(address)
        adjacency = self.adjacency_matrix[index]
        # next_closest_location_index = [float(num) for float(num) in adjacency if float(num) > 0]
        min = float(adjacency[0])
        min_index = None
        for i in range(len(adjacency)):
            if 0 < float(adjacency[i]) < min:
                min = float(adjacency[i])
                min_index = i
        return self.indices[min_index]


class Truck:
    def __init__(self, truck_number, departure_time):
        self.delivery_list = [None] * 16
        self.truck_number = truck_number
        self.count = 0
        self.mileage = 0.0
        self.hub = '4001 South 700 East'
        self.current_location = self.hub
        hours, minutes = departure_time.split(":")
        self.time = datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
        self.distance_table = AdjacencyMatrix()

    def add(self, package):
        if self.count < len(self.delivery_list):
            package.status = f'On Truck {self.truck_number} for delivery'
            self.delivery_list[self.count] = package
            self.count += 1
            return True
        return False

    def deliver(self):
        while self.count > 0:
            current_package = self.delivery_list[0]
            shortest_distance = self.distance_table.get_distance_between(self.current_location, self.delivery_list[0].address)
            for j in range(self.count):
                distance = self.distance_table.get_distance_between(self.current_location, self.delivery_list[j].address)
                if distance <= shortest_distance:
                    shortest_distance = distance
                    current_package = self.delivery_list[j]
            print(f'Traveling {shortest_distance} miles from {self.current_location} to {current_package.address}')
            self.current_location = current_package.address
            hours = shortest_distance / 18
            self.time += datetime.timedelta(hours=hours)
            self.mileage += shortest_distance
            print(f'Current mileage: {self.mileage} Current time: {self.time}')
            current_package.status = f'Delivered at {self.time}'
            self.delivery_list.pop(self.delivery_list.index(current_package))
            self.count -= 1
        distance_to_hub = self.distance_table.get_distance_between(self.current_location, self.hub)
        hours = distance_to_hub / 18
        self.time += datetime.timedelta(hours=hours)
        self.mileage += distance_to_hub
        self.delivery_list = [None] * 16



    def get_time_string(self): return self.time.strftime('%H:%M:%S')


def create_package_list():
    h = HashMap()
    with open('csv/WGUPS_Package_File.csv') as package_file:
        csv_reader = csv.reader(package_file)
        for line in csv_reader:
            notes = line[7]
            if notes == '':
                notes = None
            h.add(int(line[0]), Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], notes))
    return h


test_map = HashMap()
test_map.add([0, 'address', 'business name'],  [0, 1, 2, 3, 4])
test_map.display()
# for i in truck1_packages:
#     package_list.get(i).display()
#
# for i in truck2_packages:
#     package_list.get(i).display()

# package_list.display()

prompt = 'What would you like to do?\n1. Begin delivery simulation\n2. Lookup Package\n3. Quit\n>> '
# user_input = int(input(prompt))
user_input = 1
while True:
    if user_input == 1:
        package_list = create_package_list()

        truck1 = Truck(1, '08:00')
        truck2 = Truck(2, '08:00')
        # Load Truck 1
        truck1_packages = [1, 2, 4, 13, 14, 15, 16, 19, 20, 21, 27, 33, 34, 35, 39, 40]

        truck2_packages = [3, 5, 7, 8, 10, 11, 17, 18, 22, 23, 24, 29, 30, 36, 37, 38]

        for i in truck1_packages:
            truck1.add(package_list.get(i))

        for i in truck2_packages:
            truck2.add(package_list.get(i))

        truck1.deliver()
        truck2.deliver()

        truck1_packages = [6, 25, 26, 31, 32]
        truck2_packages = [9, 12, 28]

        for i in truck1_packages:
            truck1.add(package_list.get(i))

        package9 = package_list.get(9)
        package9.address = '410 S State St'
        package9.city = 'Salt Lake City'
        package9.state = 'UT'
        package9.zip = '84111'

        for i in truck2_packages:
            truck2.add(package_list.get(i))

        truck1.deliver()
        truck2.time = datetime.datetime.now().replace(hour=10, minute=20, second=0, microsecond=0)
        truck2.deliver()

        print(truck1.time)
        print(truck1.mileage)
        print(truck2.time)
        print(truck2.mileage)
    elif user_input == 2:
        print('Lookup')
    elif user_input == 3:
        print('Quitting')
        break
    else:
        print('Invalid input; please try again')
    user_input = int(input(prompt))
