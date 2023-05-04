from http.client import UNSUPPORTED_MEDIA_TYPE
import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    values = struct.unpack('iffffff',data)
    print(values)