# Network-Device-Inventory

A Python-based project developed as part of my Scripting 3.1 coursework at Technological University of the Shannon (TUS).

## About the Project

This program allows users to manage a simple network device inventory through a menu-driven interface. It uses Python dictionaries to store device information and provides functionality for registering, searching, updating and removing network devices.

## Features

- Register new network devices.
- Validate IPv4 addresses within the `192.168.1.1` to `192.168.1.254` range.
- Prevent duplicate device names and IP addresses.
- Search for devices by name.
- Update device operational status (Online/Offline).
- Remove devices with confirmation.
- Display all registered devices.
- Generate a network summary report.
- Save and load device information using a text file.

## Supported Device Types

- Router
- Switch
- Server
- Firewall
- Access Point

## Technologies Used

- Python
- Dictionaries
- Sets
- Functions
- Loops and conditional statements
- File handling

## How to Run

1. Download or clone this repository.
2. Make sure Python is installed.
3. Run `NetworkDeviceManager.py`.
4. Use the numbered menu options to manage network devices.

The program automatically loads previously saved device information from `network_inventory.txt` and saves changes when exiting.

