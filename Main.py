# ID: 012325580

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
    # print(f"Looking for the closest address to {location}. Visited: {visited_addresses}")

    distance_index = None
    for address in addressData:
        if location == address[2]:
            distance_index = int(address[0])
            break

    if distance_index is None:
        # print('Distance index is none')
        return None, None

    unvisited_addresses = [address for address in addressData if address[2] not in visited_addresses]
    if not unvisited_addresses:
        # print("No unvisited addresses remaining!")
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
    for i in range(1, 14):
        package = packageData.lookup(i)
        if package:
            truck1.load_package(package)

    truck2 = Truck()
    for i in range(14, 28):
        package = packageData.lookup(i)
        if package:
            truck2.load_package(package)

    truck3 = Truck()
    for i in range(28, 41):
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
    global time_str
    minutes = 0

    current_location = '4001 South 700 East'
    visited_addresses = []
    packages_delivered = 0

    while len(truck.packages) > 0:
        next_address, distance = get_distance(current_location, distances, addresses, visited_addresses)
        if next_address is None:
            # print("No valid next address, breaking loop")
            break
        # print(f"Current location: {current_location}")
        # print(f"Next address: {next_address}")

        truck.miles += distance
        minutes += calculateTime(distance)
        hours = minutes // 60
        hours += 8
        remaining_minutes = minutes % 60
        time_str = f"{int(hours):02}:{int(remaining_minutes):02}"

        packages_at_address = [p for p in truck.packages if p.address == next_address]
        for package in packages_at_address:
            package.update_status("EN ROUTE", time_str)

        current_location = next_address

        # print(f"Packages before delivery: {len(truck.packages)}")
        for package in packages_at_address:
            # print(f"Delivering Package {package.id} to {package.address}")
            truck.deliver(package, distance, time_str)
            packages_delivered += 1
        # print(f"Remaining Packages: {len(truck.packages)}")
        # print(f"Miles: {miles}, time: {minutes}")
        visited_addresses.append(current_location)

    return time_str, packages_delivered


# loading trucks
truck1, truck2, truck3 = loadTrucks(packageMap)

time, delivered = nearest_neighbor(truck1, distanceMatrix, addressMatrix)
time2, delivered2 = nearest_neighbor(truck2, distanceMatrix, addressMatrix)
time3, delivered3 = nearest_neighbor(truck3, distanceMatrix, addressMatrix)

print(f"Truck 1 ==> Miles: {round(truck1.miles, 2)}, Completed Time: {time} AM, Deliveries: {delivered}")
print(f"Truck 2 ==> Miles: {round(truck2.miles, 2)}, Completed Time: {time2} AM, Deliveries: {delivered2}")
print(f"Truck 3 ==> Miles: {round(truck3.miles, 2)}, Completed Time: {time3} AM, Deliveries: {delivered3}")

total_miles = round(truck1.miles + truck2.miles + truck3.miles, 2)
print(total_miles)



print("\n================== WGUPS ROUTING PROGRAM ==================\n")
while True:
    print("1. Print All Package Status and Total Mileage\n")
    print("2. Get a Single Package Status with a Time\n")
    print("3. Get All Package Status with a Time\n")
    print("4. Exit the Program\n")

    choice = input("Enter your choice (1-4): ")
    print()

    if choice == '1':
        for i in range(1, 41):
            package = packageMap.lookup(i)
            print(f"Package: {package.id}, Status: {package.status}")
        print(f"Total mileage: {total_miles}\n")
    elif choice == '2':
        selection = input("Enter a package ID: ")
        id = int(selection)
        if id < 1 or id > 40:
            print("Invalid package ID")
        else:
            package = packageMap.lookup(id)
            print(f"Package: {package.id}, Status: {package.status}, Time: {package.delivery_time}\n")
    elif choice == '3':
        print("")
    elif choice == '4':
        print("Exiting program...")
        break
    else:
        print("Invalid input. Please try again")
