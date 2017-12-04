from typing import List, Tuple
import math

from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import DetectedObject, TargetPoint, ObjectType

class PathFinder(AbstractLayer[List[DetectedObject], TargetPoint]):
    def call_from_upper(self, detected_objects: List[DetectedObject]) -> None:
        if self.lower is not None:
            blue_cups = PathFinder.get_objects_by_type(detected_objects, ObjectType.BLUE_CUP)
            yellow_cups = PathFinder.get_objects_by_type(detected_objects, ObjectType.YELLOW_CUP)

            if blue_cups and yellow_cups:
                nearest_blue_cup = PathFinder.get_nearest_object(blue_cups)
                nearest_yellow_cup = PathFinder.get_nearest_object(yellow_cups)

                target_point = TargetPoint(PathFinder.calculate_center_point(nearest_yellow_cup.position, nearest_blue_cup.position))

                self.call_lower(target_point)
            else:
                self.call_lower(TargetPoint((0,0)))


    def calculate_center_point(position1: Tuple[float], position2: Tuple[float]) -> Tuple[float]:
        return ((position1[0] + position2[0]) / 2, (position1[1] + position2[1]) / 2)

    def get_objects_by_type(detected_objects: List[DetectedObject], object_type: ObjectType) -> List[DetectedObject]:
        objs = []
        for obj in detected_objects:
            if obj.object_type == object_type:
                objs.append(obj)
        return objs

    def calculate_distance(detected_object: DetectedObject) -> float:
        return math.sqrt(math.pow(detected_object.position[0], 2) + math.pow(detected_object.position[1], 2))

    def get_nearest_object(objects: List[DetectedObject]) -> DetectedObject:
        nearest_object = min(objects, key=lambda obj: PathFinder.calculate_distance(obj))
        return nearest_object

    def call_from_lower(self, message: str) -> None:
        print("ERROR: PathFinder: call_from_lower not implemented")
