#!/usr/bin/env python3

# import serial
import sys
import struct
from enum import Enum

##############################################
#
# to create a new Packet do the following:
#
# 	packet = Packet()
# 	packet.mode = <mode> 			# where <mode> is one of "Mode.DRIVE" or "Mode.STEER"
# 	packet.direction = <direction> 		# where <direction> is one of "Direction.BACKWARD" or "Direction.FORWARD"
# 	packet.debug_lvl = <debug_level> 	# where <debug_lvl> is an int with: 0 <= debug_lvl < 64
# 	packet.value = <value> 			# where <value> should be better defined in the next version :P
#
# or use:
#	packet = Packet()
#	packet.setData(<mode>, <direction>, <debug_lvl>, <value>)
#
# to send this packet do:
#
# 	serial.write(packet.getData())
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

class Packet:
	mode = Mode.STEER
	direction = Direction.FORWARD
	debug_lvl = 0
	value = 0

	def setData(self, mode_, direction_, debug_lvl_, value_):
		self.mode = mode_
		self.direction = direction_
		self.debug_lvl = debug_lvl_
		self.value = value_
	def fromData(data):
		print("Packet::fromData(): TODO")
	def getData(self):
		return struct.pack("<Bi", self.getHeader(), self.getValue())
	def getHeader(self):
		header = 0
		header |= MODE_MASK if self.mode == Mode.DRIVE else NULL_MASK
		header |= DIRECTION_MASK if self.direction == Direction.BACKWARD else NULL_MASK
		header |= OPTION_MASK & self.debug_lvl
		return header

	def getValue(self):
		return int(self.value)
