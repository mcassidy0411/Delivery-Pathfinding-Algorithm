# Michael Cassidy, 009986687

import csv
from HashTable import HashTable

# Provides access to distance data in the WGUPS_Distance_Table.csv file
class AdjacencyMatrix:

    # Default Constructor.  Builds two HashTables, one containing [address, index] and another containing
    # [index, distance to all other indices] key-value pairs.  O(n)
    def __init__(self):

        # Initialize two empty HashTables
        self.address_index_hashmap = HashTable()
        self.distance_hashmap = HashTable()
        with open('csv/WGUPS_Distance_Table.csv') as distance_file:
            csv_reader = csv.reader(distance_file)
            self.adjacency_matrix = [line for line in csv_reader]

            # Iterate over each row of WGUPS_Distance_Table.csv.  O(n)
            for i in range(len(self.adjacency_matrix)):
                row = self.adjacency_matrix[i]

                # Extract and format address, stripping business name
                address = str(row.pop(0))
                new_address = address.split('\n', 1)[-1].split(',', 1)[0].strip()

                # Add [address, index] to address_index_hashmap
                self.address_index_hashmap.add(new_address, i)

                # Add [index, distance to all other indices]
                self.distance_hashmap.add(i, row)

    # Takes two address strings as input.  Finds index of each address in address_index_hashmap.
    # Finds distance between the two addresses in distance_hashmap.  O(1)
    def get_distance_between(self, point_x_str, point_y_str):
        # Get each address index
        point_x_index = int(self.address_index_hashmap.get(point_x_str))
        point_y_index = int(self.address_index_hashmap.get(point_y_str))

        # Set distance_list to the list of all distances to point_x address
        distance_list = self.distance_hashmap.get(point_x_index)

        # If the distance from x to y is blank
        if distance_list[point_y_index] == '':

            # Set distance_list to the list of all distances to point_y address
            distance_list = self.distance_hashmap.get(point_y_index)

            # return distance from y to x
            return float(distance_list[point_x_index])

        # If the distance from x to y is not blank
        else:
            # Return the distance from x to y
            return float(distance_list[point_y_index])
