# Michael Cassidy, 009986687

import TimeUtils
import datetime
from AdjacencyMatrix import AdjacencyMatrix


class Truck:
    # Default Constructor.  O(1)
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

    # Adds Package objects to self.delivery_list.  O(1)
    def add(self, package):
        # If there are 0 packages on the truck, reinitialize delivered_package_list to an empty list.  Set
        # next_departure_time equal to master_time, where master_time is the current time of the truck
        if self.count == 0:
            self.delivered_package_list = []
            self.next_departure_time = self.master_time

        # If the count of packages on the truck is less than the max length of delivery_list (16), add the Package to
        # delivery_list and increment count
        if self.count < len(self.delivery_list):
            self.delivery_list[self.count] = package
            self.count += 1
            return True
        return False

    # Core Algorithm.  Utilizes a nearest neighbor approach to determine the closest unvisited location to the current
    # location.  Delivers all packages along the path the algorithm determines.  Updates package and truck status.
    # The outer loop will iterate n times and for each iteration of the outer loop, the inner loop will iterate n times,
    # where n is the number of packages.  O(n * n) = O(n^2)
    def run_delivery_route(self):
        # This outer loop runs n + 1 times, where n equal the number of packages.  Aside from the nested for loop, all
        # operations run in O(1) time, so the worst-case (and best-case, in this instance) complexity of the outer
        # loop is O(n)
        while self.count >= 0:

            # If there are one or more packages in package_list, the algorithm in the following lines will be executed.
            if self.count != 0:

                # Set the initial value to compare as the first package in package list
                current_package = self.delivery_list[0]

                # Set the initial shortest distance to the distance between the current location and the first package
                # in package list
                shortest_distance = self.distance_table.get_distance_between(self.current_location,
                                                                                   self.delivery_list[0].address)

                # Loop through each package in package_list.  Inside this loop all operations are O(1) in the worst
                # case so the complexity of this loop is O(n)
                for j in range(self.count):

                    # Calculate the distance between the current location and the jth package in package_list
                    distance = self.distance_table.get_distance_between(self.current_location,
                                                                        self.delivery_list[j].address)

                    # If distance is less than the previously calculated shortest_distance, set shortest_distance to
                    # distance and set current_package to the corresponding package
                    if distance <= shortest_distance:
                        shortest_distance = distance
                        current_package = self.delivery_list[j]

                # Upon exiting the loop, the package with the next closest unvisited location has been identified and
                # stored in current_package.  current_location is set to the address attribute of current_package
                self.current_location = current_package.address

                # Update the truck status
                self.status = f'En Route to {self.current_location} at {self.master_time}'

                # Set the time and mileage of the truck
                self.set_time(shortest_distance)
                self.set_mileage(shortest_distance)

                # Update the current package status and time the status was modified
                current_package.status = f'Delivered'
                current_package.last_modified = self.master_time

                # Add the package to delivered_package_list, the return value of this function
                self.delivered_package_list.append(current_package)

                # Remove the current_package from delivery_list and decrement count as the package location was visited
                # and should no longer be a factor in the minimum distance calculation
                self.delivery_list.pop(self.delivery_list.index(current_package))

                # Decrement count of packages on the truck
                self.count -= 1

            # When count == 0, there are no packages in delivery_list.
            else:

                # return_to_hub() updates truck status, time and mileage and reinitializes delivery_list as an empty
                # list containing 16 ‘None’ values.  More packages can now be loaded on the truck
                self.return_to_hub()

                # Returns the list of packages that were delivered
                return self.delivered_package_list

    # Helper function calculates time as a function of distance and sets Truck member variable.  O(1)
    def set_time(self, distance):

        # Hours spent travelling = distance travelled / speed (18 MPH)
        hours = distance / 18

        # Add time calculation to Tuck's master_time
        self.master_time += datetime.timedelta(hours=hours)

    # Helper function sets Truck member variable mileage.  O(1)
    def set_mileage(self, distance):
        self.mileage += distance

    # return_to_hub() updates truck status, time and mileage and reinitializes delivery_list as an empty list
    # containing 16 ‘None’ values.  More packages can now be loaded on the truck.  O(1)
    def return_to_hub(self):
        distance_to_hub = self.distance_table.get_distance_between(self.current_location, self.hub)
        self.set_time(distance_to_hub)
        self.set_mileage(distance_to_hub)
        self.delivery_list = [None] * 16
        self.count = 0
        self.trip_number += 1
        self.status = f'Returned to Hub at {self.master_time}'
