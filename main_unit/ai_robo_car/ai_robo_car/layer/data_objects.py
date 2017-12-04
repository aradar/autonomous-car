from enum import Enum

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
    def __init__(self, position, radius, object_type):
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
