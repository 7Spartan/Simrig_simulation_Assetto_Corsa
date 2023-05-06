import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import socket
import struct
import math

# # Define the size of the car frame
# car_length = 3 # meters

# # Define the initial car frame
# car_frame = np.array([
#     [0, 0, 0],
#     [car_length, 0, 0],
#     [car_length, car_length/2, 0],
#     [car_length, car_length/2, car_length/2],
#     [car_length, 0, car_length/2],
#     [0, 0, car_length/2],
#     [0, car_length/2, car_length/2],
#     [0, car_length/2, 0]
# ])

# # Define the initial figure and axis objects
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Define the function that updates the car frame rotation
# def update_car_frame(heading, pitch, roll):
#     # Calculate the rotation matrix based on the heading, pitch, and roll angles
#     c1 = np.cos(np.deg2rad(heading))
#     s1 = np.sin(np.deg2rad(heading))
#     c2 = np.cos(np.deg2rad(pitch))
#     s2 = np.sin(np.deg2rad(pitch))
#     c3 = np.cos(np.deg2rad(roll))
#     s3 = np.sin(np.deg2rad(roll))
#     R = np.array([
#         [c1*c2, c1*s2*s3 - s1*c3, c1*s2*c3 + s1*s3],
#         [s1*c2, s1*s2*s3 + c1*c3, s1*s2*c3 - c1*s3],
#         [-s2, c2*s3, c2*c3]
#     ])
#     # Apply the rotation to the car frame and return the result
#     return np.dot(car_frame, R.T)

# Define the UDP socket parameters
UDP_IP = '127.0.0.1'
UDP_PORT = 5005

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Start the infinite loop that updates the visualization
while True:
    # Read the incoming data from the UDP socket
    data, addr = sock.recvfrom(1024)
    # Unpack the binary data using the struct module
    rpm, vel_x, vel_y, vel_z, heading, pitch, roll = struct.unpack('iffffff', data)
    # Update the car frame rotation
    # car_frame_rotated = update_car_frame(heading, pitch, roll)
    # # Clear the previous plot and plot the updated car frame
    # ax.clear()
    # ax.set_xlim([-3.14, 3.14])
    # ax.set_ylim([-1, 1])
    # ax.set_zlim([-1, 1])
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # ax.plot(car_frame_rotated[:, 0], car_frame_rotated[:, 1], car_frame_rotated[:, 2], 'o-', linewidth=2)
    # plt.draw()
    # plt.pause(0.001)
    # ax.plot([0, 1], [0, 1], [0, 1])
    # plt.draw()
    # plt.pause(0.001)
    print("heading: \t",heading * 180/math.pi)
    print("pitch: \t",pitch * 180/math.pi)
    print("roll: \t",roll * 180/math.pi)
