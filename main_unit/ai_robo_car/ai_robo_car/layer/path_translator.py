from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import TargetPoint
from ai_robo_car.layer.data_objects import EngineInstruction
import math

class PathTranslator(AbstractLayer[TargetPoint, EngineInstruction]):
    def call_from_upper(self, message: TargetPoint) -> None:
        (x, y) = message.position
        print("PathTranslator: call_from_upper ->", x, y)

        if x == 0 and y == 0:
            print("INVALID POINT:", x, y)
            return

        if x != 0:
            angle = math.atan(y / x) / math.pi * 180
        else:
            angle = 90

        if angle < -90 or angle > 90:
            print("INVALID ANGLE:", angle)
            return

        print("using angle:", angle)

        speed = math.fabs((angle + 90) / 90 - 1)
        if angle > 0:
            steer = 90 - angle
        else:
            steer = -90 - angle

        if self.lower is not None:
            self.call_lower(EngineInstruction(speed, steer))

    def call_from_lower(self, message: EngineInstruction) -> None:
        print("PathTranslator: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(str("!"))
