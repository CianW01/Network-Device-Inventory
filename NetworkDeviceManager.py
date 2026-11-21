import os

# Just makes sure the text file is saved in the same folder as this program
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Stores all registered network devices
devices = {}

# Checks if an ip address is valid and within allowed range
def validateIP(ipAddress):

    # Splits the ip address into four parts using the dots
    octets = ipAddress.split(".")

    if len(octets) != 4:
        return False

    # Checks that each part contains a number between 0 and 255
    for octet in octets:
        if not octet.isdigit():
            return False
        number = int(octet)

        if number < 0 or number > 255:
            return False

    # Checks that the ip starts with 192.168.1
    if octets[0] != "192" or octets[1] != "168" or octets[2] != "1":
        return False

    # Checks that the final number is between 1 and 254
    lastOctet = int(octets[3])

    if lastOctet < 1 or lastOctet > 254:
        return False

    return True


# Registers a new device in the inventory
def registerDevice():

    deviceName = input("Enter device name: ").strip()

    # Checks if the device name is already being used
    if deviceName in devices:
        print("Error: Device name already exists.")
        return

    ipAddress = input("Enter IP address: ").strip()

    # Checks if the ip address is valid
    if not validateIP(ipAddress):
        print("Error: IP address not in range. Arasaka firewall says no.")
        return

    #Checks if another device is already using this ip address
    for name in devices:
        if devices[name]["ip"] == ipAddress:
            print("Error: IP address is already assigned.")
            return

    # Gets the device type and checks that it is one of the allowed options
    deviceType  = input("Enter device type (Router, Switch, Server, Firewall, Access Point): ").strip().title()

    if deviceType not in ["Router", "Switch", "Server", "Firewall", "Access Point"]:
        print("Error: That ain't a device type, choom.")
        return

    # Gets the device status and checks that it is valid
    deviceStatus = input ("Enter status (Online/Offline): ").strip().title()

    if deviceStatus != "Online" and deviceStatus != "Offline":
        print("Error: Invalid status.")
        return

    # Adds the device details to the dictionary
    devices[deviceName] = {
        "ip": ipAddress,
        "type": deviceType,
        "status": deviceStatus
    }

    print("Success:", deviceName, "registered to the Net.")


# Searches for a device using its name
def searchDevice():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:

        # Displays the details of the device if it is found
        print("Name:", deviceName)
        print("IP Address:", devices[deviceName]["ip"])
        print("Type:", devices[deviceName]["type"])
        print("Status:", devices[deviceName]["status"])

    else:
        print("Error: Can't find this gon... I mean, device.")


# Updates the online or offline status of a device
def updateStatus():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:
        newStatus = input("Enter new status (Online/Offline): ").strip().title()

        # Checks that the new status is valid before updating it
        if newStatus == "Online" or newStatus == "Offline":
            devices[deviceName]["status"] = newStatus
            print("Success:", deviceName, "status updated to", newStatus)

        else:
            print("Error: Invalid status, Enter Online or Offline.")

    else:
        print("Error: Target not found.")


# Removes a device from the inventory
def removeDevice():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:
        # Asks the user to confirm before removing the device
        confirm = input("Are you sure you want to remove " + deviceName + "? (yes/no): ").strip().lower()

        if confirm == "yes":
            del devices[deviceName]
            print("Success: ", deviceName, "removed from the crew.")

        else:
            print("Device removal cancelled.")

    else:
        print("Error: Device not found.")


# Displays all registered devices and their details
def displayInventory():

    if len(devices) == 0:
        print("No devices registered.")
        return

    print("\n========== Network Inventory ==========")
    # Formats the headings and device details into columns
    print("{:<15} {:<18} {:<15} {:<10}".format("Name", "IP Address", "Type", "Status"))
    print("-" * 60)

    for deviceName in devices:
        print("{:<15} {:<18} {:<15} {:<10}".format(
            deviceName,
            devices[deviceName]["ip"],
            devices[deviceName]["type"],
            devices[deviceName]["status"]
        ))


# Creates a report showing the number and status of network devices
def summaryReport():

    totalDevices = len(devices)
    onlineDevices = 0
    offlineDevices = 0

    # Used to count how many devices belong to each type
    deviceTypes = {}
    # A set is used to keep track of the different device types
    uniqueTypes = set()

    for deviceName in devices:
        
        if devices[deviceName]["status"] == "Online":
            onlineDevices = onlineDevices + 1

        elif devices[deviceName]["status"] == "Offline":
            offlineDevices = offlineDevices + 1

        deviceType = devices[deviceName]["type"]
        uniqueTypes.add(deviceType)

        # Adds to the count if the device type already exists
        if deviceType in deviceTypes:
            deviceTypes[deviceType] = deviceTypes[deviceType] + 1

        else:
            # Starts the count at 1 for a new device type
            deviceTypes[deviceType] = 1

    # Calculates the percentage of devices that are online
    if totalDevices > 0:
        onlinePercentage = (onlineDevices / totalDevices) * 100

    else:
        onlinePercentage = 0.0

    print("\n========== NETWORK SUMMARY ==========")
    print("Total devices:", totalDevices)
    print("Online devices:", onlineDevices)
    print("Offline devices:", offlineDevices)
    print("Network availability: {:.1f}%".format(onlinePercentage))

    print("Devices by type:")

    for deviceType in deviceTypes:
        print(deviceType + ":", deviceTypes[deviceType])

    print("Unique device types:", len(uniqueTypes))


# Saves the current device information to the text file
def saveInventory():

    file = open("network_inventory.txt", "w")

    for deviceName in devices:

        ipAddress = devices[deviceName]["ip"]
        deviceType = devices[deviceName]["type"]
        deviceStatus = devices[deviceName]["status"]
        # Writes each device's details on a separate line
        file.write(deviceName + "," + ipAddress + "," + deviceType + "," + deviceStatus + "\n")

    file.close()
    print("Inventory has been saved to network_inventory.txt")
    

# Loads previously saved devices when the program starts
def loadInventory():

    try:
        file = open("network_inventory.txt", "r")
        lines = file.readlines()
        file.close()

        # Reads each line and separates the device details
        for line in lines:
            line = line.strip()
            details = line.split(",")

            # Checks that the line contains all four device details
            if len(details) == 4:
                deviceName = details[0]
                ipAddress = details[1]
                deviceType = details[2]
                deviceStatus = details[3]

                devices[deviceName] = {
                    "ip": ipAddress,
                    "type": deviceType,
                    "status": deviceStatus
                }
        print("Network inventory loaded successfully.")
        print("GOOD MORNING NIGHT CITY!")
    
    # Runs this if the text file does not exist yet
    except FileNotFoundError:
        print("No existing inventory found. Starting with an empty inventory")


# Displays the main menu and options
def displayMenu():
    print("\n========== Network Device Manager ==========")
    print("1. Register New Device")
    print("2. Search for Device")
    print("3. Update Device Status")
    print("4. Remove Device")
    print("5. Display Network Inventory")
    print("6. Network Summary Report")
    print("7. Exit")
    print("==============================================")

# Runs the main program and handles menu selections
def main():

    # Loads any previously saved devices before displaying the menu
    loadInventory()

    # Keeps the menu running until the user chooses to exit
    while True:
        
        displayMenu()

        choice = input("Enter your choice: ")
        
        if choice == "1":
            registerDevice()

        elif choice == "2":
            searchDevice()

        elif choice == "3":
            updateStatus()

        elif choice == "4":
            removeDevice()

        elif choice == "5":
            displayInventory()

        elif choice == "6":
            summaryReport()

        elif choice == "7":
            print("\nSaving inventory to the Net...")
            saveInventory()
            print("See you in the major leagues, choom.")
            break

        else:
            print("\nInvalid selection, Come on, Samurai. It's not that complicated.")

# Starts the program
main()
