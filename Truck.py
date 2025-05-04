from typing import List


class Truck:
    def __init__(self, packages: List['Package'] = None):
        self.packages = packages if packages else []
        self.miles = 0
        self.speed = 18
        self.capacity = 16
        self.location = "HUB"
        self.delivered_packages = []

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)

    def deliver(self, package, distance, time):
        if package in self.packages:
            self.packages.remove(package)
            self.delivered_packages.append(package)
            self.miles += distance
            package.update_status('DELIVERED', time)
            self.location = package.address
            # print(f"Package {package.id} is being removed from truck")

    def print_packages(self):
        for package in self.packages:
            print(package.__str__())

    def package_count(self):
        return len(self.packages)

    def __str__(self):
        return (f"Truck location: {self.location}, "
                f"Miles driven: {self.miles}, "
                f"# of packages: {len(self.packages)}")
