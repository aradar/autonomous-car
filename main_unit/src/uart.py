#!/usr/bin/env python3

import serial
dev = '/dev/ttyS0'
baud = 9600

ser = serial.Serial(dev)
print('set serial device to: ' + str(dev))

ser.baudrate = baud
print('configure baudrate to: ' + str(baud))

send_data = bytes('Hi', 'utf-8')
ser.write(send_data)
print('send data: ' + str(send_data))

rcv_data = ser.read(len(send_data))
print('received data: ' + str(rcv_data))


ser.close()
