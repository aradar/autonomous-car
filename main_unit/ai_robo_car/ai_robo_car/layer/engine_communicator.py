import logging
from pprint import pformat

import serial
import socket
import math
from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import EngineInstruction
from ai_robo_car.packet import Packetizer, Side, Direction

logger = logging.getLogger(__name__)


class EngineCommunicator(AbstractLayer[EngineInstruction, None]):
    def __init__(self, upper: AbstractLayer, lower: AbstractLayer, is_test_communication=False):
        super(EngineCommunicator, self).__init__(upper, lower)
        self.is_test_communication = is_test_communication
        if self.is_test_communication:
            self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ser.connect(('127.0.0.1', 8000))
        else:
            self.ser = serial.Serial('/dev/ttyS0')
            self.ser.baudrate = 9600

    def call_from_upper(self, engine_instruction: EngineInstruction) -> None:
        if self.ser is not None:
            if engine_instruction is None:
                # Todo: send break
                return

            side = Side.LEFT if engine_instruction.steer < 0 else Side.RIGHT
            direction = Direction.BACKWARD if engine_instruction.speed < 0 else Direction.FORWARD
            steer = math.fabs(engine_instruction.steer)
            speed = math.fabs(engine_instruction.speed)

            data = Packetizer.create_data(side, direction, 0, steer, speed)
            logger.debug("produced {}".format(pformat(data)))
            if self.is_test_communication:
                self.ser.send(data)
            else:
                self.ser.write(data)

    def call_from_lower(self, message: str) -> None:
        print("EngineCommunicator: call_from_lower -> " + message)
        if self.upper is not None:
            self.upper.call_upper(message + str("!"))

    def close(self):
        self.ser.close()
