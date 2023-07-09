# Michael Cassidy, 009986687

class HashTable:
    # Constructor
    def __init__(self):
        self.size = 8
        self.map = [None] * self.size
        self.number_of_items = 0

    # TODO just use hashing function
    def generate_hash(self, key):
        # hash = 0
        # for char in str(key):
        #     hash += ord(char)
        return hash(key) % self.size

    def add(self, key, value):
        key_hash = self.generate_hash(key)
        key_value = [key, value]
        self.number_of_items += 1
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
        key_hash = self.generate_hash(key)
        if self.map[key_hash] is not None:
            for item in self.map[key_hash]:
                if item[0] == key:
                    return item[1]
        return None

    def delete(self, key):
        key_hash = self.generate_hash(key)

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
