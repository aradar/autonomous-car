#!/usr/bin/env python3

import serial
import sys
import struct
from enum import Enum

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
	value = 0.0

	def fromData(data):
		print("Packet::fromData(): TODO")
	def getHeader(self):
		data = 0
		data |= MODE_MASK if self.mode == Mode.DRIVE else NULL_MASK
		data |= DIRECTION_MASK if self.direction == Direction.BACKWARD else NULL_MASK
		data |= OPTION_MASK & self.debug_lvl
		print("data = ", data)
		# data.append(bytes(struct.pack("f", float(self.value))))
		return data

	def getValue(self):
		return struct.pack("f", self.value)

packet = Packet()
packet.mode = Mode.STEER
packet.direction = Direction.FORWARD
packet.debug_lvl = 2
packet.value = 33.4
serial.write(packet.getHeader())
serial.write(packet.getValue())
