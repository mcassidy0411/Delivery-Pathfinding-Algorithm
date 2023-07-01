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

    def get_adjacency(self, address):
        for i in range(len(self.indices)):
            if address == self.indices[i]:
                return self.adjacency_matrix[i]

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
    def __init__(self, truck_number):
        self.package_list = [None] * 16
        self.truck_number = truck_number
        self.count = 0

    def add(self, package):
        if self.count < len(self.package_list):
            package.status = f'On Truck {self.truck_number} for delivery'
            self.package_list[self.count] = package
            self.count += 1
            return True
        return False

    def deliver(self):
        if self.package_list[self.count] is not None:
            self.package_list.pop(self.count)
            return True
        return False


# def next_closest():
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
truck1 = Truck(1)
truck1.add(package_list.get(1))
truck1.deliver()
package_list.get(1).display()

