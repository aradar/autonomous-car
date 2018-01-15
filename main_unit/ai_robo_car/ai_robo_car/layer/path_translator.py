import logging
import math
from pprint import pformat

from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import TargetPoint
from ai_robo_car.layer.data_objects import EngineInstruction

logger = logging.getLogger(__name__)


class PathTranslator(AbstractLayer[TargetPoint, EngineInstruction]):
    def call_from_upper(self, target_point: TargetPoint) -> None:
        if self.lower is None:
            return

        engine_instruction = None
        if target_point is not None:

            (x, y) = target_point.position

            steer = 0
            speed = 0

            # 0 <= threshold <= 90
            threshold_angle = 45

            if y >= 0 and ((x != 0) or (y != 0)):
                if y == 0:
                    if x > 0:
                        angle = 0
                    else:
                        angle = 180
                elif x != 0:
                    angle = math.atan(y / x) / math.pi * 180
                else:
                    angle = 90

                if angle < 0:
                    angle = 180 + angle

                # threshold
                if angle < 0 or angle > 180:
                    logger.error("angle ({}) is invalid!".format(angle))
                    angle = 90
                elif 0 <= angle < 90 - threshold_angle:
                    angle = threshold_angle
                elif 90 + threshold_angle < angle <= 180:
                    angle = 90 + threshold_angle

                if angle > 0:
                    steer = 90 - angle
                elif angle < 0:
                    steer = -90 - angle
                speed = 1 - (math.fabs(steer) / threshold_angle)
                speed = 0.5 + 0.5 * speed
                engine_instruction = EngineInstruction(speed, steer)

        logger.debug("produced {}".format(pformat(engine_instruction)))
        self.call_lower(engine_instruction)

    def call_from_lower(self, message: EngineInstruction) -> None:
        print("PathTranslator: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(str("!"))
