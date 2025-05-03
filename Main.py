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


# def distance_function:
# takes current position and maps a distance to every other address
# returns the address with the smallest distance

# while truck has packages
# look through truck packages
# find the nearest package address to the current position: distance_function(current position)
# update package status to ETA
# set current position to that address
# add miles to truck
# set the delivery time and status as DELIVERED
# remove package from truck package list


def find_nearest_address(truck, current_location, distance_function):
    nearest_package = None
    nearest_distance = float('inf')

    for package in truck.packages:
        distance = distance_function(current_location, package.address)

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_package = package

    return nearest_package, nearest_distance


def nearest_neighbor(truck1, distance_function):
    current_location = "HUB"

    while truck1.package_count() > 0:
        nearest_package, nearest_distance = find_nearest_address(truck1, current_location, distances)
        nearest_package.updateStatus("DELIVERED")

        truck1.deliver(nearest_package, nearest_distance, datetime.time)
        current_location = nearest_package.address
