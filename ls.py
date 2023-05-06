import sys
import ac
import acsys 
import platform
import os

try:
    if platform.architecture()[0] == "64bit":
        sysdir='apps/python/ls/stdlib64'
    else:
        sysdir='apps/python/ls/stdlib'
    sys.path.insert(0, sysdir)
    os.environ['PATH'] = os.environ['PATH'] + ";."
except Exception as e:
    ac.log("*ls: Error importing libraries: %s" % e)

from sim_info import info
import locale
locale.setlocale(locale.LC_ALL, '')
import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

ac.console("\n UDP target IP: %s" % UDP_IP)
ac.console("\n UDP target port; %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ls_lapcount = 0
ls_rpms=0
ls_velocity_1 = 0.0
ls_velocity_2 = 0.0
ls_velocity_3 = 0.0
lapcount = 0
ls_heading = 0.0
ls_pitch = 0.0
ls_roll = 0.0

def acMain(ac_version):
    global ls_lapcount, ls_rpms, ls_velocity_1, ls_velocity_2, ls_velocity_3, ls_heading, ls_pitch, ls_roll

    appWindow = ac.newApp("ls")
    ac.setSize(appWindow, 200, 400)
    ac.setTitle(appWindow,"LooseScrews Telemetry data")

    ac.log("\n**ls: Hello, Assetto Corsa application world!")
    ac.console("\n**ls: Hello, Assetto Corsa console!")

    ls_lapcount = ac.addLabel(appWindow,"Laps: 0")
    ls_rpms = ac.addLabel(appWindow,"rpms: 0")
    ls_velocity_2 = ac.addLabel(appWindow,"vel_y: 0")
    ls_velocity_3 = ac.addLabel(appWindow,"vel_z: 0")
    ls_velocity_1 = ac.addLabel(appWindow,"vel_x: 0")
    ls_heading = ac.addLabel(appWindow,"heading: 0")
    ls_pitch = ac.addLabel(appWindow,"pitch: 0")
    ls_roll = ac.addLabel(appWindow,"roll: 0")

    ac.setPosition(ls_lapcount, 3 ,30)
    ac.setPosition(ls_rpms,3 ,60)
    ac.setPosition(ls_velocity_1,3 ,90)
    ac.setPosition(ls_velocity_2,3 ,120)
    ac.setPosition(ls_velocity_3,3 ,150)
    ac.setPosition(ls_heading,3 ,180)
    ac.setPosition(ls_pitch,3 ,210)
    ac.setPosition(ls_roll,3 ,240)

    return "ls"

def acUpdate(deltaT):
    global ls_lapcount, lapcount, ls_rpms, ls_velocity_1, ls_velocity_2, ls_velocity_3, ls_heading, ls_pitch, ls_roll, UDP_IP, UDP_PORT
    laps = ac.getCarState(0,acsys.CS.LapCount)
    rpms = str(info.physics.rpms)
    velocity_2 = str(info.physics.velocity[0])
    velocity_3 = str(info.physics.velocity[1])
    velocity_1 = str(info.physics.velocity[2])
    heading = str(info.physics.heading)
    pitch = str(info.physics.pitch)
    roll = str(info.physics.roll)

    ac.setText(ls_rpms, "rpms: {}".format(rpms))
    ac.setText(ls_velocity_1, "vel_x: {}".format(velocity_1))
    ac.setText(ls_velocity_2, "vel_y: {}".format(velocity_2))
    ac.setText(ls_velocity_3, "vel_z: {}".format(velocity_3))
    ac.setText(ls_heading, "heading: {}".format(heading))
    ac.setText(ls_pitch, "pitch: {}".format(pitch))
    ac.setText(ls_roll, "roll: {}".format(roll))

    if laps > lapcount:
        lapcount = laps
        ac.setText(ls_lapcount, "Laps: {}".format(lapcount))

    data = struct.pack('iffffff', info.physics.rpms, info.physics.velocity[2], info.physics.velocity[0], info.physics.velocity[1], info.physics.heading, info.physics.pitch, info.physics.roll)

    sock.sendto(data,(UDP_IP, UDP_PORT))

def acShutdown(*args):
    sock.close()