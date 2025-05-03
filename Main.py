from Truck import Truck
from Package import Package
import csv
import datetime

from HashTable import HashTable

with open("data/package.csv") as packageData:
    packages = csv.reader(packageData)
    next(packages)
    packages = list(packages)

with open("data/addresses.csv") as addressData:
    addresses = csv.reader(addressData)
    addresses = list(addresses)

with open("data/distances.csv") as distanceData:
    distances = csv.reader(distanceData)
    distances = list(distances)


def loadPackageData(data, map):
    for row in data:
        p = Package(*row)
        map.insert(row[0], p)
    return map


packageMap = loadPackageData(packages, HashTable())


def loadTrucks(packageData):
    truck1 = Truck()
    for i in range(1, 17):
        package = packageData.lookup(i)
        if package:
            truck1.load_package(package)

    truck2 = Truck()
    for i in range(17, 33):
        package = packageData.lookup(i)
        if package:
            truck2.load_package(package)

    truck3 = Truck()
    for i in range(33, 40):
        package = packageData.lookup(i)
        if package:
            truck3.load_package(package)

    return truck1, truck2, truck3


truck1, truck2, truck3 = loadTrucks(packageMap)
truck1.print_packages()
truck2.print_packages()
truck3.print_packages()
