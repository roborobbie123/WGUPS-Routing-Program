# HashTable class using chaining.
from Package import Package


class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):  # does both insert and update
        key = int(key)

        bucket_index = hash(key) % len(self.table)
        selected_bucket = self.table[bucket_index]

        for entry_index in range(len(selected_bucket)):
            existing_key = selected_bucket[entry_index][0]
            if existing_key == key:
                selected_bucket[entry_index] = (key, item)
                return

        selected_bucket.append((key, item))

    def search(self, id):

        bucket_index = hash(id) % len(self.table)
        selected_bucket = self.table[bucket_index]

        for item in selected_bucket:
            key = item[0]
            package = item[1]
            if key == id:
                return package

        return None

    def remove(self, id):
        bucket_index = hash(id) % len(self.table)
        selected_bucket = self.table[bucket_index]

        for item_index in range(len(selected_bucket)):
            key = selected_bucket[item_index][0]
            if key == id:
                del selected_bucket[item_index]
                return True

        return False

    def print_map(self):
        for i, bucket in enumerate(self.table):
            print(f"Bucket {i}:")
            for key, obj in bucket:
                print(f"  ID: {key} ====> [{obj}]")
