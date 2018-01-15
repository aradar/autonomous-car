from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import EngineInstruction
from ai_robo_car.packet import Packetizer, Side, Direction
import serial
import socket
import math


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
            if engine_instruction is None:
                # Todo: send break
                return

            side = Side.LEFT if engine_instruction.steer < 0 else Side.RIGHT
            direction = Direction.BACKWARD if engine_instruction.speed < 0 else Direction.FORWARD
            steer = math.fabs(engine_instruction.steer)
            speed = math.fabs(engine_instruction.speed)

            data = Packetizer.create_data(side, direction, 0, steer, speed)
            if self.is_test_communication:
                self.ser.send(data)
            else:
                self.ser.write(data)

    def call_from_lower(self, message: str) -> None:
        print("EngineCommunicator: call_from_lower -> " + message)
        if self.upper is not None:
            self.upper.call_upper(message + str("!"))

    def close(self):
        """
        Closes the serial port
        """
        self.ser.close()
