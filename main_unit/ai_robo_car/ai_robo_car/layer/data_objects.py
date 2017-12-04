from enum import Enum
from typing import Tuple


class ObjectType(Enum):
    UNDEFINED_OBJECT = 0
    BLUE_CUP = 1
    YELLOW_CUP = 2


class BoundingBox:
    def __init__(self, left, right, top, bottom, width, height, object_type):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.height = height
        self.width = width
        self.object_type = object_type


class DetectedObject:
    """
    Represents the detected objects relative to the position of the camera. The origin of the coordinate system is
    the position of the camera and the unit of measure is defined by the RelativeTranslator layer.
    """

    def __init__(self, position: Tuple[float, float], radius: float, object_type : ObjectType):
        """
        :param position: relative position of the center of the object
        :param radius: radius of the object
        :param object_type: type of the detected object
        """

        self.position = position
        self.radius = radius
        self.object_type = object_type


class TargetPoint:
    def __init__(self, position):
        self.position = position


class EngineInstruction:
    def __init__(self, speed, steer):
        self.speed = speed
        self.steer = steer
