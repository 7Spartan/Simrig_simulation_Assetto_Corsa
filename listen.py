import numpy as np
import socket
import struct
import math
import threading
import queue
import time
from bluetooth import *

# Define the UDP socket parameters
UDP_IP = '127.0.0.1'
UDP_PORT = 5005

# Create the UDP socket
UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_sock.bind((UDP_IP, UDP_PORT))
print("Waiting... \n")

###############BLUETOOTH###################
# HC-06 Bluetooth module MAC address
bluetooth_address = 'FC:A8:9A:00:19:68' 
bluetooth_port = 1  # RFCOMM port number
bluetooth_passkey = '1234'  # Pairing passkey

# Create a lock to synchronize access to the Bluetooth socket
bluetooth_lock = threading.Lock()

# Define the size of the car frame
car_length = 3  # meters

# Define the initial car frame
car_frame = np.array([
    [0, 0, 0],
    [car_length, 0, 0],
    [car_length, car_length/2, 0],
    [car_length, car_length/2, car_length/2],
    [car_length, 0, car_length/2],
    [0, 0, car_length/2],
    [0, car_length/2, car_length/2],
    [0, car_length/2, 0]
])

# Define the thread-safe queue to store UDP data
udp_data_queue = queue.Queue(maxsize=1)

# Define the function that updates the car frame rotation
def update_car_frame(heading, pitch, roll):
    c1 = np.cos(heading)
    s1 = np.sin(heading)
    c2 = np.cos(pitch)
    s2 = np.sin(pitch)
    c3 = np.cos(roll)
    s3 = np.sin(roll)
    R = np.array([
        [c1*c2, c1*s2*s3 - s1*c3, c1*s2*c3 + s1*s3],
        [s1*c2, s1*s2*s3 + c1*c3, s1*s2*c3 - c1*s3],
        [-s2, c2*s3, c2*c3]
    ])
    return np.dot(car_frame, R.T)

def udp_data_reception():
    while True:
        try:
            data, addr = UDP_sock.recvfrom(12)
            heading, pitch, roll = struct.unpack('fff', data)
            with udp_data_queue.mutex:
                udp_data_queue.queue.clear()  # Clear the queue to keep only the latest data
            udp_data_queue.put((heading, pitch, roll), block=False)
            print("UDP: heading: {}".format(heading), "... {}".format(float(heading)))
        except socket.error as e:
            print(f"UDP data reception error: {e}")
            break

def process_udp_data():
    while True:
        try:
            heading, pitch, roll = udp_data_queue.get(block=True)
            # Process the received data here
            car_frame_rotated = update_car_frame(float(heading), float(pitch), float(roll))
            # Perform any other required operations
        except queue.Empty:
            pass

def bluetooth_data_transmission():
    try:
        # Create Bluetooth socket and connect to HC-06 module
        bluetooth_sock = BluetoothSocket(RFCOMM)
        bluetooth_sock.settimeout(30)
        bluetooth_sock.connect((bluetooth_address, bluetooth_port))
        print("Bluetooth connection established!")

        # Pair with HC-06 module using the passkey
        bluetooth_sock.setblocking(True)
        try:
            bluetooth_sock.send(str(bluetooth_passkey))
            print("Pairing with HC-06 module...")
            time.sleep(5)  # Wait for the pairing process to complete
        except BluetoothError as e:
            print(f"Pairing failed: {e}")
            bluetooth_sock.close()
            return

        while True:
            #Get the latest UDP data from the queue
            try:
                heading, pitch, roll = udp_data_queue.get(block=True)
                # Process the received data here
                # Send data to HC-06 module
                with bluetooth_lock:
                    if(heading > 0):
                        bluetooth_sock.send("LED ON")
                        # print("LED ON")
                        # Receive data from HC-06 module
                        data = bluetooth_sock.recv(1024)
                        print(f"[HC-06]: {data.decode('utf-8')}")
                        # time.sleep(0.1)
                    else:
                        # Send data to HC-06 module
                        bluetooth_sock.send("LED OFF")
                        # print("LED OFF")
                        # Receive data from HC-06 module
                        data = bluetooth_sock.recv(1024)
                        print(f"[HC-06]: {data.decode('utf-8')}")
                        # time.sleep(0.1)
            except queue.Empty:
                pass


    except BluetoothError as e:
        print(f"Bluetooth communication error: {e}")
        return

    finally:
        bluetooth_sock.close()

# Start the UDP data reception thread
udp_thread = threading.Thread(target=udp_data_reception)
udp_thread.daemon = True
udp_thread.start()

# Start the data processing thread
data_processing_thread = threading.Thread(target=process_udp_data)
data_processing_thread.daemon = True
data_processing_thread.start()

# Start the Bluetooth data transmission thread
bluetooth_thread = threading.Thread(target=bluetooth_data_transmission)
bluetooth_thread.daemon = True
bluetooth_thread.start()

# Main thread continues to do other
while True:
    # Perform any other tasks here
    # ...
    # Example: Sleep for 1 second
    time.sleep(0.1)