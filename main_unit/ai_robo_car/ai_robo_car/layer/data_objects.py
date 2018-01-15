from enum import Enum
from typing import Tuple


class ObjectType(Enum):
    """
    0 - defines a undefined object
    1 - a blue cup
    2 - a yellow cup
    """
    UNDEFINED_OBJECT = 0
    BLUE_CUP = 1
    YELLOW_CUP = 2


class BoundingBox:
    def __init__(self, left, right, top, bottom, width, height, object_type):
        """
        A BoundingBox defines the size, location in pixels and the ObjectType of an object.
        :param left: the left side of the object, relative of the whole image
        :param right: the right side of the object, relative of the whole image
        :param top: the top side of the object, relative of the whole image
        :param bottom: the bottom side of the object, relative of the whole image
        :param width: the width of the object
        :param height: the height of the object
        :param object_type: the object type
        """
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = width
        self.height = height
        self.object_type = object_type

    def __str__(self):
        return "BoundingBox: left {}, right {}, top {}, bottom {}, width {}, height {}, object_type {}".format(
            self.left, self.right, self.top, self.bottom, self.width, self.height, self.object_type)


class DetectedObject:
    """
    Represents the detected objects relative to the position of the camera. The origin of the coordinate system is
    the position of the camera and the unit of measure is defined by the RelativeTranslator layer.
    """

    def __init__(self, position: Tuple[float, float], radius: float, object_type: ObjectType):
        """
        :param position: relative position of the center of the object
        :param radius: radius of the object
        :param object_type: type of the detected object
        """
        self.position = position
        self.radius = radius
        self.object_type = object_type

    def __str__(self):
        return "DetectedObject: position {}, radius {}, objects_type {}".format(
            self.position, self.radius, self.object_type)


class TargetPoint:
    """
    Represents the position the car should drive on the current state.
    """
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return "TargetPoint: position {}".format(self.position)


class EngineInstruction:
    """
    Represents the speed and steer the car should drive on the current state.
    """
    def __init__(self, speed, steer):
        self.speed = speed
        self.steer = steer

    def __str__(self):
        return "EngineInstruction: speed {}, steer {}".format(self.speed, self.steer)
