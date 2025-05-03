from Truck import Truck
from Package import Package
import csv
import datetime

from HashTable import HashTable

with open("data/package.csv") as packageData:
    packages = csv.reader(packageData)
    next(packages)
    packages = list(packages)

with open("data/distances.csv") as distanceData:
    distances = csv.reader(distanceData)
    distances = list(distances)

with open("data/addresses.csv") as addressData:
    addresses = csv.reader(addressData)
    addresses = list(addresses)


def loadPackageData(data, map):
    for row in data:
        p = Package(*row)
        map.insert(row[0], p)
    return map


def loadDistanceData(data, matrix):
    for row in data:
        converted_row = [float(val) if val else None for val in row]
        matrix.append(converted_row)
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] is None and matrix[j][i] is not None:
                matrix[i][j] = matrix[j][i]


def loadAddressData(data, matrix):
    for row in data:
        matrix.append(row)


def get_distance(location, distanceData, addressData, visited_addresses):
    print(f"Looking for the closest address to {location}. Visited: {visited_addresses}")

    distance_index = None
    for address in addressData:
        if location == address[2]:
            distance_index = int(address[0])
            break

    if distance_index is None:
        print('Distance index is none')
        return None, None

    unvisited_addresses = [address for address in addressData if address[2] not in visited_addresses]
    if not unvisited_addresses:
        print("No unvisited addresses remaining!")
        return None, None

    nearest_distance = float('inf')
    address_index = None
    nearest_address = None

    for address in unvisited_addresses:
        addr_index = int(address[0])
        distance = distanceData[distance_index][addr_index]
        if 0 < distance < nearest_distance:
            nearest_distance = distance
            nearest_address = address[2]

    return nearest_address, nearest_distance


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


def calculateTime(distance):
    time = distance / 18.0
    minutes = time * 60
    return minutes


# loads package.csv to a hash map
packageMap = loadPackageData(packages, HashTable())

# loads distances.csv to a list
distanceMatrix = []
loadDistanceData(distances, distanceMatrix)

# loads address.csv to a list
addressMatrix = []
loadAddressData(addresses, addressMatrix)


def nearest_neighbor(truck, distances, addresses):
    miles = 0
    time = 0
    current_location = '4001 South 700 East'
    visited_addresses = []

    while len(truck.packages) > 0:
        next_address, distance = get_distance(current_location, distances, addresses, visited_addresses)
        if next_address is None:
            print("No valid next address, breaking loop")
            break
        print(f"Current location: {current_location}")
        print(f"Next address: {next_address}")

        packages_at_address = [p for p in truck.packages if p.address == next_address]

        current_location = next_address
        miles += distance
        time += calculateTime(distance)

        print(f"Packages before delivery: {len(truck.packages)}")
        for package in packages_at_address:
            print(f"Delivering Package {package.id} to {package.address}")
            truck.deliver(package, distance, time)
        print(f"Remaining Packages: {len(truck.packages)}")
        print(f"Miles: {miles}, time: {time}")
        visited_addresses.append(current_location)

    return miles, time


# loading trucks
truck1, truck2, truck3 = loadTrucks(packageMap)

miles, time = nearest_neighbor(truck1, distanceMatrix, addressMatrix)
miles2, time2 = nearest_neighbor(truck2, distanceMatrix, addressMatrix)
miles3, time3 = nearest_neighbor(truck3, distanceMatrix, addressMatrix)

print(f"Truck 1 Miles: {miles}")
print(f"Truck 1 Time: {time} minutes")
print(f"Truck 2 Miles: {miles2}")
print(f"Truck 2 Time: {time2} minutes")
print(f"Truck 3 Miles: {miles3}")
print(f"Truck 3 Time: {time3} minutes")

