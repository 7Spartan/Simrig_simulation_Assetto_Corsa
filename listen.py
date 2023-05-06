import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import socket
import struct
import math
import ctypes
from ctypes import c_int32, c_float, c_wchar
# # Define the size of the car frame
car_length = 3 # meters

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

# # Define the initial figure and axis objects
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# # Define the function that updates the car frame rotation
def update_car_frame(heading, pitch, roll):
#     # Calculate the rotation matrix based on the heading, pitch, and roll angles
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
#     # Apply the rotation to the car frame and return the result
    return np.dot(car_frame, R.T)

# Define the UDP socket parameters
UDP_IP = '127.0.0.1'
UDP_PORT = 5005

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
# Start the infinite loop that updates the visualization
print("Waiting... \n")
while True:
    # Read the incoming data from the UDP socket
    data, addr = sock.recvfrom(12)
    # Unpack the binary data using the struct module
    heading, pitch, roll = struct.unpack('fff', data)
    # Update the car frame rotation
    # car_frame_rotated = update_car_frame(c_float(heading), c_float(pitch), c_float(roll))
    car_frame_rotated = update_car_frame(float(heading), float(pitch), float(roll))
    # car_frame = car_frame_rotated
    # # Clear the previous plot and plot the updated car frame
    # ax.clear()
    # ax.set_xlim([-3.14, 3.14])
    # ax.set_ylim([-2, 2])
    # ax.set_zlim([-2, 2])
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # ax.plot(car_frame_rotated[:, 0], car_frame_rotated[:, 1], car_frame_rotated[:, 2], 'o-', linewidth=2)

    # plt.draw()
    # plt.pause(0.001)
    print("heading: {}".format(heading), "... {}".format(float(heading)))
    # print("pitch: \t",pitch * 180/math.pi)
    # print("roll: \t",roll * 180/math.pi)
