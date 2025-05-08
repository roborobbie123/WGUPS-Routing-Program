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


def get_distance(location, distanceData, addressData, packageAddresses, visited_addresses):
    # print(f"Looking for the closest address to {location}. Visited: {visited_addresses}")

    distance_index = None
    for address in addressData:
        if location == address[2]:
            distance_index = int(address[0])
            break

    if distance_index is None:
        # print('Distance index is none')
        return None, None

    unvisited_addresses = []
    for address in addressData:
        if address[2] not in visited_addresses and address[2] in packageAddresses:
            unvisited_addresses.append(address)

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
    truck1_packages = [14, 15, 16, 34, 25, 26, 24, 22, 19, 20, 21, 35, 36, 37, 9]
    for num in truck1_packages:
        package = packageData.lookup(num)
        package.set_truck(1)
        truck1.load_package(package)

    truck2 = Truck()
    truck2_packages = [23, 27, 28, 29, 30, 31, 32, 33, 38, 39, 40, 17, 18]
    for num in truck2_packages:
        package = packageData.lookup(num)
        package.set_truck(2)
        truck2.load_package(package)

    truck3 = Truck()
    truck3_packages = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13]
    for num in truck3_packages:
        package = packageData.lookup(num)
        package.set_truck(3)
        truck3.load_package(package)

    return truck1, truck2, truck3


def calculateTime(distance):
    time = distance / 18.0
    minutes = time * 60

    return minutes


def nearest_neighbor(truck, distances, addressData):
    time_str = ''
    minutes = 0  # Time since 8:00 AM

    current_location = '4001 South 700 East'
    visited_addresses = []
    packages_delivered = 0

    special_package_id = '9'
    special_package_time = 140

    late_packages = ['6', '25', '28', '32']
    late_package_time = 65

    for package in truck.packages:
        package.update_status("EN ROUTE")

    # === Phase 1: Deliver all packages except Package 9 ===
    while any(p.id != special_package_id and p.id not in late_packages for p in truck.packages):

        # Only consider addresses with packages not including package 9
        eligible_packages = [p for p in truck.packages if p.id != special_package_id and p.id not in late_packages]
        address_set = {p.address for p in eligible_packages}

        next_address, distance = get_distance(current_location, distances, addressData, address_set, visited_addresses)
        if next_address is None:
            print("No valid next address, breaking loop")
            break

        minutes += calculateTime(distance)
        hours = minutes // 60 + 8
        remaining_minutes = minutes % 60
        time_str = f"{int(hours):02}:{int(remaining_minutes):02}"

        packages_at_address = [p for p in truck.packages if p.address == next_address and p.id != special_package_id and p.id not in late_packages]

        current_location = next_address

        for package in packages_at_address:
            truck.deliver(package, minutes)
            packages_delivered += 1
            print(package.id)

        visited_addresses.append(current_location)
        truck.miles += distance
        print(f"Delivered to {current_location}. Load: {len(truck.packages)}. Time: {time_str}")

    # === Phase 2: Deliver Package 9 after 10:20 AM ===
    remaining_packages = [p for p in truck.packages if p.id == special_package_id or p.id in late_packages]
    for remaining_package in remaining_packages:
        if remaining_package:
            if remaining_package.id == special_package_id:
                if minutes < special_package_time:
                    wait_minutes = special_package_time - minutes
                    minutes += wait_minutes
                    print(f"Waiting until 10:20 AM to deliver Package 9...")
            if remaining_package.id in late_packages:
                if minutes < late_package_time:
                    wait_minutes = late_package_time - minutes
                    minutes += wait_minutes
                    print(f"Waiting until 9:05 AM to deliver Package...")

        # Find distance to its address
        next_address, distance = get_distance(current_location, distances, addressData, {remaining_package.address}, [])
        if next_address:
            minutes += calculateTime(distance)
            truck.miles += distance
            current_location = next_address
            hours = minutes // 60 + 8
            remaining_minutes = minutes % 60
            time_str = f"{int(hours):02}:{int(remaining_minutes):02}"
            truck.deliver(remaining_package, minutes)
            packages_delivered += 1
            print(f"Delivered Package 9 to {current_location} at {time_str}")

    return time_str, packages_delivered


# loads package.csv to a hash map
packageMap = loadPackageData(packages, HashTable())

# loads distances.csv to a list
distanceMatrix = []
loadDistanceData(distances, distanceMatrix)

# loads address.csv to a list
addressMatrix = []
loadAddressData(addresses, addressMatrix)

# loading trucks
truck1, truck2, truck3 = loadTrucks(packageMap)

time, delivered = nearest_neighbor(truck1, distanceMatrix, addressMatrix)
time2, delivered2 = nearest_neighbor(truck2, distanceMatrix, addressMatrix)
time3, delivered3 = nearest_neighbor(truck3, distanceMatrix, addressMatrix)

print(f"Truck 1 ==> Miles: {round(truck1.miles, 2)}, Completed Time: {time} AM, Deliveries: {delivered}")
print(f"Truck 2 ==> Miles: {round(truck2.miles, 2)}, Completed Time: {time2} AM, Deliveries: {delivered2}")
print(f"Truck 3 ==> Miles: {round(truck3.miles, 2)}, Completed Time: {time3} AM, Deliveries: {delivered3}")

total_miles = round(truck1.miles + truck2.miles + truck3.miles, 2)


# for row in distanceMatrix:
#     print(row)
#
# for row in addressMatrix:
#     print(row)

def get_time_in_minutes(time_type):
    while True:
        # Prompt user for time input in HH:MM format
        user_input = input(f"Please enter the {time_type} time in HH:MM format: ")

        # Error check for correct format (HH:MM)
        if len(user_input) == 5 and user_input[2] == ':':
            hours_str, minutes_str = user_input.split(':')

            # Validate if hours and minutes are numeric and within valid ranges
            if hours_str.isdigit() and minutes_str.isdigit():
                hours = int(hours_str)
                minutes = int(minutes_str)

                if 0 <= hours <= 23 and 0 <= minutes <= 59:
                    # Convert to minutes since midnight
                    total_minutes = hours * 60 + minutes
                    return total_minutes
                else:
                    print("Invalid time range. Hours should be between 00-23 and minutes between 00-59.")
            else:
                print("Invalid input. Please ensure hours and minutes are numeric.")
        else:
            print("Invalid format. Please enter time in HH:MM format.")


print("\n================== WGUPS ROUTING PROGRAM ==================\n")
while True:
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time")
    print("4. Package status by time")
    print("5. Exit the Program\n")

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
            print(f"Package: {package.id}, Status: {package.status}, Time: {package.delivery_time_formatted}\n")
    elif choice == '3':
        for i in range(1, 41):
            package = packageMap.lookup(i)
            print(f"Package: {package.id}, Address: {package.address}, Deadline: {package.deadline}, Status: {package.status}, Time: {package.delivery_time_formatted}, Truck: {package.truck}")
    elif choice == '4':
        minutes = get_time_in_minutes("end") - 480
        hours = ((minutes + 480) // 60) % 24  # Keep it within 24 hours
        mins = minutes % 60
        print(f"Status of packages at {hours:02}:{mins:02}")

        for i in range(1, 41):
            package = packageMap.lookup(i)
            if package.delivery_time <= minutes:
                print(f"Package: {package.id}, Address: {package.address}, Deadline: {package.deadline}, Status: {package.status}, Time: {package.delivery_time_formatted}, Truck: {package.truck}")
            else:
                print(f"Package: {package.id} Status: EN ROUTE Deadline: {package.deadline}")
    elif choice == '5':
        print("Exiting program...")
        break
    else:
        print("Invalid input. Please try again")
