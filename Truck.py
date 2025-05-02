class Truck:
    def __init__(self, packages, miles):
        self.packages = packages
        self.miles = miles
        self.speed = 18
        self.capacity = 16
        self.location = "HUB"

    def load_packages(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    def deliver(self, package, distance, time):
        if package in self.packages:
            self.packages.remove(package)
            self.miles += distance
            package.updateStatus('Delivered', time)
            self.location = package.address



