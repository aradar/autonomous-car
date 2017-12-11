#!/usr/bin/env python3

# import serial
from serial import Serial
import sys
import struct
from enum import Enum

##############################################
#
# to create data you can send via serial do the following:
#
# 	data = Packetizer.create_data(<side>, <direction>, <debug_lvl>, <value_steer>, <value_speed>)   # where <side> is one of "Side.LEFT" or "Side.RIGHT"
# 									 	                        # where <direction> is one of "Direction.BACKWARD" or "Direction.FORWARD"
# 									 	                        # where <debug_lvl> is an int with: 0 <= debug_lvl < 64
# 									 	                        # where <value_steer> is the angle of the wheels (left: -90° - 0°; right: 0° - 90°)
#                                                                                                       # where <value_speed> is the speed in m/s
# then you can send "data" via serial:
#
# 	ser.write(data)
#
# or, if you want to send, directly use:
#
#	Packetizer.write_data(<serial>, <side>, <direction>, <debug_lvl>, <value_steer>, <value_speed>) # where serial is the serial port over which the data should be sent
#
##############################################

NULL_MASK 	= 0b00000000
SIDE_MASK 	= 0b10000000
DIRECTION_MASK 	= 0b01000000
OPTION_MASK 	= 0b00111111

class Side(Enum):
    LEFT = 0
    RIGHT = 1

class Direction(Enum):
    BACKWARD = 0
    FORWARD = 1 

class Packetizer:
    def create_header(side: Side, direction: Direction, debug_lvl: int):
        header = 0
        header |= SIDE_MASK if side == Side.RIGHT else NULL_MASK
        header |= DIRECTION_MASK if direction == Direction.FORWARD else NULL_MASK
        header |= OPTION_MASK & debug_lvl
        return header

    def create_data(side: Side, direction: Direction, debug_lvl: int, value_steer: float, value_speed: float):
        header = Packetizer.create_header(side, direction, debug_lvl)
        return struct.pack("<Bff", header, value_steer, value_speed)

    def write_data(serial: Serial, side: Side, direction: Direction, debug_lvl: int, value_steer: float, value_speed: float):
        serial.write(Packetizer.create_data(side, direction, debug_lvl, value_steer, value_speed))
