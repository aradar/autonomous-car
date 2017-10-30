#!/usr/bin/env python3

import serial
import sys
from packet import *
import struct

dev = '/dev/ttyS0'
baud = 9600

ser = serial.Serial(dev)
print('set serial device to: ' + str(dev))

ser.baudrate = baud
print('configure baudrate to: ' + str(baud))

if len(sys.argv) is 3:
    control_type = str(sys.argv[1])
    control_value = float(sys.argv[2]) 
    byte_values = struct.pack('f', control_value)
    
    if control_type == '-d': # drive
        packet = Packet()
        packet.setData(Mode.DRIVE, Direction.BACKWARD, 3, control_value);
        ser.write(packet.getData())
    elif control_type == '+d':
        packet = Packet()
        packet.setData(Mode.DRIVE, Direction.FORWARD, 5, control_value);
        ser.write(packet.getData())
    elif control_type == '+s': # steer
        packet = Packet()
        packet.setData(Mode.STEER, Direction.FORWARD, 7, control_value);
        ser.write(packet.getData())
    elif control_type == '-s': 
        packet = Packet()
        packet.setData(Mode.STEER, Direction.BACKWARD, 42, control_value);
        ser.write(packet.getData())

    ser.write(byte_values)
    print('send data: ' + str(byte_values))
   
    for i in range(5):
        rcv_data = ser.read()
        print('received data: ' + str(rcv_data))

    print(ser.readline())

else:
    print('undefined arguments')
    
ser.close()
