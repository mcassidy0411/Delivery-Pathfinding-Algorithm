# Michael Cassidy, 009986687


import csv
from HashMap import HashMap


class AdjacencyMatrix:
    def __init__(self):
        self.address_index_hashmap = HashMap()
        self.distance_hashmap = HashMap()
        with open('csv/WGUPS_Distance_Table.csv') as distance_file:
            csv_reader = csv.reader(distance_file)
            self.adjacency_matrix = [line for line in csv_reader]

            for i in range(len(self.adjacency_matrix)):
                # Puts address in the correct format and moves to indices list.
                # This list will look up index by address and vice versa
                row = self.adjacency_matrix[i]
                address = str(row.pop(0))
                new_address = address.split('\n', 1)[-1].split(',', 1)[0].strip()
                self.address_index_hashmap.add(new_address, i)
                self.distance_hashmap.add(i, row)

    def get_distance_between(self, point_x_str, point_y_str):
        point_x_index = int(self.address_index_hashmap.get(point_x_str))
        point_y_index = int(self.address_index_hashmap.get(point_y_str))

        distance_list = self.distance_hashmap.get(point_x_index)
        if distance_list[point_y_index] == '':
            distance_list = self.distance_hashmap.get(point_y_index)
            return float(distance_list[point_x_index])
        else:
            return float(distance_list[point_y_index])
