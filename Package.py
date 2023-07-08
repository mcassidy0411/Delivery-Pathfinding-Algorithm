# Michael Cassidy, 009986687

import datetime


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
        self.last_modified = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    def get_data(self):
        return [self.status, self.last_modified, self.package_id, self.address, self.city, self.state, self.zip_code,
                self.deadline, self.weight]
