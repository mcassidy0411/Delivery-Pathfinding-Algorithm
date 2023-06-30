import re

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
        key_value = [value]

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
                if item[0].package_id == key:
                    return item[0]
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
            h.add(line[0], Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], notes))
    return h


def create_adjacency_matrix():
    with open('csv/WGUPS_Distance_Table.csv') as distance_file:
        csv_reader = csv.reader(distance_file)
        adjacency_matrix = [line for line in csv_reader]
        indices = [None] * len(adjacency_matrix)

        for i in range(len(adjacency_matrix)):
            # Puts address in the correct format and moves to indices list.
            # This list will look up index by address and vice versa
            row = adjacency_matrix[i]
            address = str(row.pop(0))
            new_address = address.split('\n', 1)[-1].split(',', 1)[0].strip()
            indices[i] = new_address

            iterator = 1
            for j in range(len(adjacency_matrix)):
                if adjacency_matrix[i][j] == '':
                    adjacency_matrix[i][j] = adjacency_matrix[i + iterator][j - iterator]
                    iterator += 1
        for i in range(len(adjacency_matrix)):
            print(adjacency_matrix[i])


create_adjacency_matrix()
# package_list = create_package_list()
# package_list.display()
# package = package_list.get(3)
# display_package(package)
