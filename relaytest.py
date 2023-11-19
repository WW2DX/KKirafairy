import socket
import time

relay_ip = "192.168.1.100"  # Your relay module IP address should be the same.
relay_port = 6722

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_module():
    # Connect to the relay module
    sock.connect((relay_ip, relay_port))

def close_relay(relay_num):
    # Turn off the specified relay
    command = "2" + relay_num
    sock.sendall(command.encode())
    print("Relay", relay_num, "turned off")
    print_relay_status()

def open_relay(relay_num):
    # Turn on the specified relay
    command = "1" + relay_num
    sock.sendall(command.encode())
    print("Relay", relay_num, "turned on")
    print_relay_status()

def print_relay_status():
    sock.sendall("00".encode())
    relay_status = sock.recv(8).decode()
    print("Relay Status:", relay_status)


# Connect to the relay module
connect_module()

# Turn on relay 1
open_relay("1")
time.sleep(1)  # Wait for 1 second

# Turn off relay 1
close_relay("1")
time.sleep(1)  # Wait for 1 second

# Turn on relay 2
open_relay("2")
time.sleep(1)  # Wait for 1 second

# Turn off relay 2
close_relay("2")
time.sleep(1)  # Wait for 1 second

# Close the socket
sock.close()
