from pixy import *
from ctypes import *
from ai_robo_car.abstract_layer import AbstractLayer
import time

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks_count = 100
blocks = BlockArray(blocks_count)
frame  = 0

class ObjectRecognizer(AbstractLayer[str, str]):
    def __init__(self, upper: AbstractLayer, lower: AbstractLayer):
        super().__init__(upper, lower)
        pixy_init()

    def call_from_upper(self, message: str) -> None:
        for i in range(20):
            print("Test")
            count = pixy_get_blocks(blocks_count, blocks)
            # Blocks found #
            if count > 0:
                print("block found")
            time.sleep(0.5)
    def call_from_lower(self, message: str) -> None:
        print("ObjectRecognizer: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(message + str("!"))

