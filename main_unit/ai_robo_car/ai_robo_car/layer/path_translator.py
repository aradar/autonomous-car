from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import TargetPoint
from ai_robo_car.layer.data_objects import EngineInstruction
import math


class PathTranslator(AbstractLayer[TargetPoint, EngineInstruction]):
    def call_from_upper(self, message: TargetPoint) -> None:
        (x, y) = message.position
        print("PathTranslator: call_from_upper ->", x, y)

        steer = 0
        speed = 0
        threshold_angle = 30
        if (x != 0) or (y != 0):

            if x != 0:
                angle = (math.atan(y / x) * 180) / math.pi
            else:
                angle = 90

            if angle < -90 or angle > 90:
                print("INVALID ANGLE:", angle)
                angle = 0
            elif 0 > angle > -threshold_angle:
                angle = -threshold_angle
            elif 0 < angle < threshold_angle:
                angle = threshold_angle

            print("using angle:", angle)

            speed = math.fabs((angle + 90) / 90 - 1)
            if angle > 0:
                steer = 90 - angle
            elif angle < 0:
                steer = -90 - angle

        if self.lower is not None:
            self.call_lower(EngineInstruction(speed, steer))

    def call_from_lower(self, message: EngineInstruction) -> None:
        print("PathTranslator: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(str("!"))
