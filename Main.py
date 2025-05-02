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

packageMap = HashTable()


def loadPackageData(data):
    for row in data:
        p = Package(*row)
        packageMap.insert(row[0], p)
    packageMap.print_map()

def loadDistanceData(data):

def loadAddressData(data):