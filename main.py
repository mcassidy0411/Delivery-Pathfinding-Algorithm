import datetime
import csv
import time


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
            self.indices = [None] * len(self.adjacency_matrix)

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

    def get_adjacency_between(self, point_a, point_b):
        list = self.get_adjacency_list(point_a)
        index = self.get_address_index(point_b)
        print(index)
        print(f'Point A: {point_a}\nPoint B: {point_b}\nDistance: {list[index]}')
        return list[index]

    def get_address_index(self, address): return self.indices.index(address)

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
        self.delivery_list = [[None, None] for _ in range(16)]
        self.truck_number = truck_number
        self.count = 0
        self.mileage = 0.0
        hours, minutes = departure_time.split(":")
        self.time = datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)

    def add(self, package, distance_to_next):
        if self.count < len(self.delivery_list):
            package.status = f'On Truck {self.truck_number} for delivery'
            row = self.delivery_list[self.count]
            row[0] = float(distance_to_next)
            row[1] = package
            self.count += 1
            print("Package added to Truck")
            return True
        return False

    def deliver(self):
        # TODO fix this
        if self.delivery_list[self.count] is not None:
            row = self.delivery_list[0]
            print(row)
            miles = row[0]
            print(f'miles {miles}')
            seconds = (miles/18) * 3600
            self.mileage += miles
            self.time = self.time + datetime.timedelta(seconds=seconds)
            print(f'miles: {self.mileage} time: {self.get_time_string()}')

            self.delivery_list.pop(self.count)
            return True
        return False

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


def time_tracker():
    time_object = time.localtime()
    print(time_object)
    local_time = time.strftime("%H:%M:%S", time_object)
    print(local_time)
    start_time = time.strftime('%H:%M:%S', time.strptime('08:00:00', '%H:%M:%S'))  # keep this
    print(start_time)


time_tracker()
am = AdjacencyMatrix()
package_list = create_package_list()
# adjacency_matrix.h.display()
# print(am.get_address_index(package_list.get(package_list.get(1).address)))
# print(am.get_address_index('195 W Oakland Ave'))
# print(type(package_list.get(1).address))
# print(am.indices)
# print(package_list.get(1).address)
# print(am.get_adjacency('195 W Oakland Ave'))
# print(am.get_next_closest('195 W Oakland Ave'))
# package_list.display()
# package = package_list.get(3)
# display_package(package)
truck1 = Truck(1, '08:00')
hub = '4001 South 700 East'
package1 = package_list.get(1)
adjacency1 = am.get_adjacency_between(hub, package1.address)
# package2_address = am.get_next_closest(package_list.get(1).address)
# print(f'next: {package2_address}')
truck1.add(package1, adjacency1)
truck1.deliver()
package_list.get(1).status = "Delivered"
package_list.get(1).display()

