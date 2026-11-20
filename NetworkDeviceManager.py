import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

devices = {}

def validateIP(ipAddress):

    octets = ipAddress.split(".")

    if len(octets) != 4:
        return False

    for octet in octets:
        if not octet.isdigit():
            return False
        number = int(octet)

        if number < 0 or number > 255:
            return False

    if octets[0] != "192" or octets[1] != "168" or octets[2] != "1":
        return False

    lastOctet = int(octets[3])

    if lastOctet < 1 or lastOctet > 254:
        return False

    return True


def registerDevice():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:
        print("Error: Device name already exists.")
        return

    ipAddress = input("Enter IP address: ").strip()

    if not validateIP(ipAddress):
        print("Error: Invalid IP address.")
        return

    for name in devices:
        if devices[name]["ip"] == ipAddress:
            print("Error: IP address is already assigned.")
            return

    deviceType  = input("Enter device type (Router, Switch, Server, Firewall, Access Point): ").strip().title()

    if deviceType not in ["Router", "Switch", "Server", "Firewall", "Access Point"]:
        print("Error: Invalid device type.")
        return

    deviceStatus = input ("Enter status (Online/Offline): ").strip().title()

    if deviceStatus != "Online" and deviceStatus != "Offline":
        print("Error: Invalid status.")
        return

    devices[deviceName] = {
        "ip": ipAddress,
        "type": deviceType,
        "status": deviceStatus
    }

    print("Success:", deviceName, "has been registered.")


def searchDevice():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:

        print("Name:", deviceName)
        print("IP Address:", devices[deviceName]["ip"])
        print("Type:", devices[deviceName]["type"])
        print("Status:", devices[deviceName]["status"])

    else:
        print("Error: Device not found.")


def updateStatus():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:
        newStatus = input("Enter new status (Online/Offline): ").strip().title()

        if newStatus == "Online" or newStatus == "Offline":
            devices[deviceName]["status"] = newStatus
            print("Success:", deviceName, "status updated to", newStatus)

        else:
            print("Error: Invalid status, Enter Online or Offline.")

    else:
        print("Error: Device not found.")


def removeDevice():

    deviceName = input("Enter device name: ").strip()

    if deviceName in devices:
        confirm = input("Are you sure you want to remove " + deviceName + "? (yes/no): ").strip().lower()

        if confirm == "yes":
            del devices[deviceName]
            print("Success: ", deviceName, "has been removed.")

        else:
            print("Device removal cancelled.")

    else:
        print("Error: Device not found.")


def displayInventory():

    if len(devices) == 0:
        print("No devices registered.")
        return

    print("\n========== Network Inventory ==========")
    print("{:<15} {:<18} {:<15} {:<10}".format("Name", "IP Address", "Type", "Status"))
    print("-" * 60)

    for deviceName in devices:
        print("{:<15} {:<18} {:<15} {:<10}".format(
            deviceName,
            devices[deviceName]["ip"],
            devices[deviceName]["type"],
            devices[deviceName]["status"]
        ))


def summaryReport():

    totalDevices = len(devices)
    onlineDevices = 0
    offlineDevices = 0

    deviceTypes = {}
    uniqueTypes = set()

    for deviceName in devices:
        
        if devices[deviceName]["status"] == "Online":
            onlineDevices = onlineDevices + 1

        elif devices[deviceName]["status"] == "Offline":
            offlineDevices = offlineDevices + 1

        deviceType = devices[deviceName]["type"]
        uniqueTypes.add(deviceType)

        if deviceType in deviceTypes:
            deviceTypes[deviceType] = deviceTypes[deviceType] + 1

        else:
            deviceTypes[deviceType] = 1

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


def saveInventory():

    file = open("network_inventory.txt", "w")

    for deviceName in devices:

        ipAddress = devices[deviceName]["ip"]
        deviceType = devices[deviceName]["type"]
        deviceStatus = devices[deviceName]["status"]
        file.write(deviceName + "," + ipAddress + "," + deviceType + "," + deviceStatus + "\n")

    file.close()
    print("Inventory has been saved to network_inventory.txt")
    

def loadInventory():

    try:
        file = open("network_inventory.txt", "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()
            details = line.split(",")

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

    except FileNotFoundError:
        print("No existing inventory found. Starting with an empty inventory")


# Menu display function
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


def main():

    loadInventory()

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
            print("\nSaving network inventory...")
            saveInventory()
            print("Goodbye!")
            break

        else:
            print("\nInvalid selection, Please try again.")

main()