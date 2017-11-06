#!/usr/bin/env python3

import serial
import sys
from packet import *
import struct

dev = '/dev/ttyS0'
baud = 9600

ser = serial.Serial(dev)
#print('set serial device to: ' + str(dev))

ser.baudrate = baud
#print('configure baudrate to: ' + str(baud))

if len(sys.argv) is 4:
    control_type = str(sys.argv[1])
    control_value = float(sys.argv[2]) 
    debug_level = int(sys.argv[3])
    
    if control_type == '-d': # drive
        #print("control_type = -d")
        packet = Packet()
        packet.setData(Mode.DRIVE, Direction.BACKWARD, debug_level, control_value);
        ser.write(packet.getData())
    elif control_type == '+d':
        #print("control_type = +d")
        packet = Packet()
        packet.setData(Mode.DRIVE, Direction.FORWARD, debug_level, control_value);
        ser.write(packet.getData())
    elif control_type == '+s': # steer
        #print("control_type = +s")
        packet = Packet()
        packet.setData(Mode.STEER, Direction.FORWARD, debug_level, control_value);
        ser.write(packet.getData())
    elif control_type == '-s': 
        #print("control_type = -s")
        packet = Packet()
        packet.setData(Mode.STEER, Direction.BACKWARD, debug_level, control_value);
        ser.write(packet.getData())
#else:
    #print('usage [+d/-d/+s/-s] <control_value> <debug_level>')
    
ser.close()
