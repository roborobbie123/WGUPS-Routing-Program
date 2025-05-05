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
        self.delivery_time = None  # in minutes since 8:00 AM
        self.delivery_time_formatted = None

    def update_status(self, update, time=None):
        self.status = update
        if time:
            self.delivery_time = time
            hours = 8 + (self.delivery_time // 60)
            minutes = self.delivery_time % 60
            self.delivery_time_formatted = f"{int(hours):02}:{int(minutes):02}"

    def __str__(self):
        return (
            f"Package ID: {self.id}, Address: {self.address}, City: {self.city}, "
            f"Zip: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, "
            f"Status: {self.status}, Delivery Time: {self.delivery_time_formatted}"
        )
