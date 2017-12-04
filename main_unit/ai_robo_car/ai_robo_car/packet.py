#!/usr/bin/env python3

# import serial
import sys
import struct
from enum import Enum

##############################################
#
# to create data you can send via serial do the following:
#
# 	data = Packetizer.create_data(<mode>, <direction>, <debug_lvl>, <value>) # where <mode> is one of "Mode.DRIVE" or "Mode.STEER"
# 									 	 # where <direction> is one of "Direction.BACKWARD" or "Direction.FORWARD"
# 									 	 # where <debug_lvl> is an int with: 0 <= debug_lvl < 64
# 									 	 # where <value> should be better defined in the next version :P
# then you can send "data" via serial:
#
# 	ser.write(data)
#
# or, if you want to send, directly use:
#
#	Packetizer.write_data(<serial>, <mode>, <direction>, <debug_lvl>, <value>) # where serial is the serial port over which the data should be sent
#
##############################################

NULL_MASK 	= 0b00000000
MODE_MASK 	= 0b10000000
DIRECTION_MASK 	= 0b01000000
OPTION_MASK 	= 0b00111111

class Mode(Enum):
	STEER = 0
	DRIVE = 1

class Direction(Enum):
	FORWARD = 0
	BACKWARD = 1

class Packetizer:
	def create_header(mode, direction, debug_lvl):
		header = 0
		header |= MODE_MASK if self.mode == Mode.DRIVE else NULL_MASK
		header |= DIRECTION_MASK if self.direction == Direction.BACKWARD else NULL_MASK
		header |= OPTION_MASK & self.debug_lvl
		return header

	def create_value(value):
		return int(value)

	def create_data(mode, direction, debug_lvl, value):
		header = create_header(mode, direction, debug_lvl)
		val = create_value(value)
		return struct.pack("<Bi", header, val)

	def write_data(serial, mode, direction, debug_lvl, value):
		serial.write(create_data(mode, direction, debug_lvl, value))
