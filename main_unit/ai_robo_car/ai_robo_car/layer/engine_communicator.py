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
    """
    The EngineCommunicator handles the serial communication between main unit and car controls (car engine).
    """

    def __init__(self, upper: AbstractLayer, lower: AbstractLayer, is_test_communication=False):
        """
        :param upper: the upper layer, most of the time the PathTranslator
        :param lower: should be None by default
        :param is_test_communication: set only be true when the function is called by a test
        """
        super(EngineCommunicator, self).__init__(upper, lower)
        self.is_test_communication = is_test_communication
        if self.is_test_communication:
            self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ser.connect(('127.0.0.1', 8000))
        else:
            self.ser = serial.Serial('/dev/ttyS0')
            self.ser.baudrate = 9600


    def call_from_upper(self, engine_instruction: EngineInstruction) -> None:
        """
        called by the upper layer, most of the time PathTranslator
        :param engine_instruction: gets a single EngineInstruction that gets packed and send over serial
        :return: None
        """
        if self.ser is not None:
            data = None
            if engine_instruction is None:
                data = self.package_engine_instruction(EngineInstruction(0., 0.))  # break
            else:
                data = self.package_engine_instruction(engine_instruction)

            if data is not None:
                logger.debug("produced {}\n".format(pformat(data)))
                if self.is_test_communication:
                    self.ser.send(data)
                else:
                    self.ser.write(data)

    def package_engine_instruction(self, engine_instruction):
        side = Side.LEFT if engine_instruction.steer < 0 else Side.RIGHT
        direction = Direction.BACKWARD if engine_instruction.speed < 0 else Direction.FORWARD
        steer = math.fabs(engine_instruction.steer)
        speed = math.fabs(engine_instruction.speed)
        data = Packetizer.create_data(side, direction, 0, steer, speed)
        return data

    def call_from_lower(self, message: str) -> None:
        print("EngineCommunicator: call_from_lower -> " + message)
        if self.upper is not None:
            self.upper.call_upper(message + str("!"))

    def close(self):
        """
        Closes the serial port
        """
        self.ser.close()

    def send_break(self) -> None:
        if self.ser is not None:
            logger.info("breaking (paused/stopped)")
            data = self.package_engine_instruction(EngineInstruction(0., 0.))
            if self.is_test_communication:
                self.ser.send(data)
            else:
                self.ser.write(data)

    def pause(self) -> None:
        self.send_break()

    def stop(self) -> None:
        self.send_break()

    def resume(self) -> None:
        data = Packetizer.create_reset_data()
        if self.is_test_communication:
            self.ser.send(data)
        else:
            self.ser.write(data)
