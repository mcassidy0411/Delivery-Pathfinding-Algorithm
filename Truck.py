# Michael Cassidy, 009986687

import TimeUtils
import datetime
from AdjacencyMatrix import AdjacencyMatrix


class Truck:
    def __init__(self, truck_number, departure_time):
        self.delivery_list = [None] * 16
        self.truck_number = truck_number
        self.count = 0
        self.mileage = 0.0
        self.hub = '4001 South 700 East'
        self.current_location = self.hub
        self.next_departure_time = TimeUtils.parse_time_string(departure_time)
        self.master_time = self.next_departure_time
        self.distance_table = AdjacencyMatrix()
        self.trip_number = 0
        self.status = 'At Hub'
        self.delivered_package_list = []

    def add(self, package):
        if self.count == 0:
            self.delivered_package_list = []
            self.next_departure_time = self.master_time
        if self.count < len(self.delivery_list):
            # package.status = f'On Truck {self.truck_number} for delivery'
            self.delivery_list[self.count] = package
            self.count += 1
            return True
        return False

    # Core Algorithm.  Utilizes a nearest neighbor approach to determine the closest unvisited location to the current
    # location.  Delivers all packages along the path the algorithm determines.  Updates package and truck status.
    # The outer loop will iterate n times and for each iteration of the outer loop, the inner loop will iterate n times,
    # where n is the number of packages.  O(n * n) = O(n^2)
    def run_delivery_route(self):
        # self.count and delivery_list are equal to the number of packages on the truck, so while self.count is greater
        # than or equal to 0, iterate this loop
        while self.count >= 0:
            if self.count != 0:
                # Set initial value for the package and the distance between that package and the current location for
                # algorithm to compare
                current_package = self.delivery_list[0]
                shortest_distance = self.distance_table.get_distance_between(self.current_location,
                                                                                   self.delivery_list[0].address)

                # For each Package in the
                for j in range(self.count):
                    distance = self.distance_table.get_distance_between(self.current_location,
                                                                        self.delivery_list[j].address)
                    if distance <= shortest_distance:
                        shortest_distance = distance
                        current_package = self.delivery_list[j]

                self.current_location = current_package.address
                self.status = f'En Route to {self.current_location} at {self.master_time}'
                self.set_time(shortest_distance)
                self.set_mileage(shortest_distance)
                current_package.status = f'Delivered'
                current_package.last_modified = self.master_time

                self.delivered_package_list.append(current_package)

                self.delivery_list.pop(self.delivery_list.index(current_package))
                self.count -= 1
            else:
                self.return_to_hub()
                return self.delivered_package_list

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
