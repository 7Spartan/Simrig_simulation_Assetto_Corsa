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
lapcount = 0

def acMain(ac_version):
    global ls_lapcount, ls_rpms

    appWindow = ac.newApp("ls")
    ac.setSize(appWindow, 200, 200)
    ac.setTitle(appWindow,"LooseScrews Telemetry data")

    ac.log("\n**ls: Hello, Assetto Corsa application world!")
    ac.console("\n**ls: Hello, Assetto Corsa console!")

    ls_lapcount = ac.addLabel(appWindow,"Laps: 0")
    ls_rpms = ac.addLabel(appWindow,"rpms: 0")
    ac.setPosition(ls_lapcount, 3 ,30)
    ac.setPosition(ls_rpms,3 ,60)
    return "ls"

def acUpdate(deltaT):
    global ls_lapcount, lapcount, ls_rpms, UDP_IP, UDP_PORT
    laps = ac.getCarState(0,acsys.CS.LapCount)
    rpms = str(info.physics.rpms)
    ac.setText(ls_rpms, "rpms: {}".format(rpms))
    if laps > lapcount:
        lapcount = laps
        ac.setText(ls_lapcount, "Laps: {}".format(lapcount))
        ac.setText(ls_rpms, "rpms: {}".format(rpms))
    sock.sendto(rpms.encode("utf-8"),(UDP_IP, UDP_PORT))

def acShutdown(*args):
    sock.close()