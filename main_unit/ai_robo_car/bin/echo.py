#!/usr/bin/env python3

import os
import sys
import time
import struct
import serial

from ai_robo_car.packet import Packetizer, Side, Direction

dev = '/dev/ttyS0'
baud = 9600
timeout = 1.0

print("")

ser = serial.Serial(dev)
print('set serial device to: ' + str(dev))

ser.baudrate = baud
print('configure baudrate to: ' + str(baud))

# timeout
#ser.timeout = timeout
#print('configure timeout to: ' + str(timeout))

#ser.write("hello".encode())

counter = 0

print("")
while True:
    #print("output:\n\n", ser.read(4), "\n")
    bytecode = ser.read(4)
    if bytecode:
        counter += 1
        print(counter, ". output: ", struct.unpack("<f", bytecode)[0], sep="")
        if (counter % 11 == 0):
            print("--")

            
ser.close()
