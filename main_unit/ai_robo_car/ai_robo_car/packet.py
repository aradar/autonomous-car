#!/usr/bin/env python3

import struct
from enum import Enum

from serial import Serial

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
##############################################

NULL_MASK = 0b00000000
SIDE_MASK = 0b10000000
DIRECTION_MASK = 0b01000000
RESTART_MASK = 0b00100000
OPTION_MASK = 0b00011111


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class Direction(Enum):
    BACKWARD = 0
    FORWARD = 1


class Packetizer:
    @staticmethod
    def create_header(side: Side, direction: Direction, debug_lvl: int, is_restart: bool):
        header = 0
        header |= SIDE_MASK if side == Side.RIGHT else NULL_MASK
        header |= DIRECTION_MASK if direction == Direction.FORWARD else NULL_MASK
        header |= RESTART_MASK if is_restart else NULL_MASK
        header |= OPTION_MASK & debug_lvl
        return header

    @staticmethod
    def create_data(side: Side, direction: Direction, debug_lvl: int, value_steer: float, value_speed: float,
                    is_restart: bool = False):
        header = Packetizer.create_header(side, direction, debug_lvl, is_restart)
        return struct.pack("<Bff", header, value_steer, value_speed)

    @staticmethod
    def create_reset_data():
        return Packetizer.create_data(Side.RIGHT, Direction.FORWARD, debug_lvl=0,
                                      value_speed=0.0, value_steer=0.0, is_restart=True)