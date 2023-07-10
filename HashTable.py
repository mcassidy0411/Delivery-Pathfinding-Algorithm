# Michael Cassidy, 009986687

# Custom HashTable data structure built using lists.  Collisions are handled by chaining.
class HashTable:
    # Default Constructor.  O(1)
    def __init__(self):
        self.size = 8
        self.map = [None] * self.size
        self.number_of_items = 0

    # Hash function uses the Python function hash() to generate an integer hash of the object passed into it.  O(1)
    def generate_hash(self, key):
        # The index the key-value pair should be stored in is the modulus of the key hash and the size of the HashTable
        return hash(key) % self.size

    # Insertion function adds key-value pairs to hash table.  On average, the complexity should be constant time but in
    # the unlikely event that all keys are hashed to the same index, the else condition would need to loop over every
    # item in the HashTable, therefore, worst-case is O(n)
    def add(self, key, value):

        # Generate key hash
        key_hash = self.generate_hash(key)

        # store key-value pair to list
        key_value = [key, value]

        # Increment number_of_items in HashTable
        self.number_of_items += 1

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True

        # Uses Chaining for when inserting a key-value pair and the index of the list already contains one or more
        # key-value pairs
        else:

            # If a key already exists at the index, iterate over all key-value pairs at this index
            for item in self.map[key_hash]:
                # If the key is the same as the key at the index, update the value and return
                if item[0] == key:
                    item[1] = value
                    return True

            # If the above condition is never True and the key doesn't exist anywhere in this index, append the
            # key-value pair to the end of the list at this index
            self.map[key_hash].append(key_value)
            return True

    # Retrieval function takes the key as input, gets the hash of the key and retrieves the key-value pair from the
    # hashed index of the table.  Like the add() function, on average, the complexity should be near constant time but
    # in the unlikely event that all keys are hashed to the same index, the loop would need to iterate over every
    # item in the HashTable until the key is found, therefore, worst-case is O(n)
    def get(self, key):

        # Get key hash to determine index the key-value pair is stored in
        key_hash = self.generate_hash(key)

        # If the index is not empty
        if self.map[key_hash] is not None:

            # Iterate over all items in the index until the key is found.  Return the value
            for item in self.map[key_hash]:
                if item[0] == key:
                    return item[1]

        # If nothing was found, return None
        return None

    # Deletion function takes the key as input, gets the hash of the key and finds the key-value pair from the
    # hashed index of the table.  Like the add() and get() functions, on average, the complexity should be near
    # constant time but in the unlikely event that all keys are hashed to the same index, the loop would need to
    # iterate over every item in the HashTable until the key is found, therefore, worst-case is O(n)
    def delete(self, key):

        # Get the key hash
        key_hash = self.generate_hash(key)

        # If the hashed index is empty, return False
        if self.map[key_hash] is None:
            return False

        # Iterate over every value at the hashed index until the key is found
        for i in range(0, len(self.map[key_hash])):

            # If the key is found, remove the key-value pair from the list and return true
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    # Iterate over every index of the HastTable and print to console.  O(n)
    def display(self):
        for item in self.map:
            if item is not None:
                print(str(item))
