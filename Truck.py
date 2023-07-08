# Michael Cassidy, 009986687


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
        self.next_departure_time = self.parse_time_string(departure_time)
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
            package.status = f'On Truck {self.truck_number} for delivery'
            self.delivery_list[self.count] = package
            self.count += 1
            return True
        return False

    def deliver_next(self):
        if self.count != 0:
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

            self.set_time(shortest_distance)
            self.set_mileage(shortest_distance)
            current_package.status = f'Delivered'
            current_package.last_modified = self.master_time

            self.delivered_package_list.append(current_package)

            self.delivery_list.pop(self.delivery_list.index(current_package))
            self.count -= 1
            return current_package
        else:
            self.return_to_hub()

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

    def parse_time_string(time):
        try:
            hours, minutes = time.split(":")
            return datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
        except AttributeError:
            return None
