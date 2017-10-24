#!/usr/bin/env python3

import serial
import sys
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
    
    if control_type == '-a':
        ser.write(bytes('a', 'utf-8'))
    elif control_type == '-s': 
        ser.write(bytes('s', 'utf-8'))

    ser.write(byte_values)
    print('send data: ' + str(byte_values))
   
    for i in range(5):
        rcv_data = ser.read()
        print('received data: ' + str(rcv_data))

    print(ser.readline())

else:
    print('undefined arguments')
    
ser.close()

