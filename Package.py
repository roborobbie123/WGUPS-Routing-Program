class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.deadline = deadline
        self.status = "At hub"
        self.delivery_time = None

    def update_status(self, update, time):
        self.status = update
        if time:
            self.delivery_time = time



    def __str__(self):
        return f"Package ID: {self.id}, Address: {self.address}, City: {self.city}, Zip: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, Delivery Time: {self.delivery_time}"
