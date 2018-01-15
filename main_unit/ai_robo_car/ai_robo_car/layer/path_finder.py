from typing import List, Tuple
import math

from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import DetectedObject, TargetPoint, ObjectType


class PathFinder(AbstractLayer[List[DetectedObject], TargetPoint]):
    """
    The PathFinder calculates a point: (float, float) where the car should go to as next step.
    This point is given in the Relative Coordinate System.
    """

    def call_from_upper(self, detected_objects: List[DetectedObject]) -> None:
        """
        gets called by the upper layer, in most reasons by the relative translator

        :detected_objects a list of all detected objects that are produced by the relative translator
        """

        if self.lower is not None:
            if detected_objects is None:
                self.call_lower(None)
                return

            blue_cups = PathFinder.get_objects_by_type(detected_objects, ObjectType.BLUE_CUP)
            yellow_cups = PathFinder.get_objects_by_type(detected_objects, ObjectType.YELLOW_CUP)

            if blue_cups and yellow_cups:
                nearest_blue_cup = PathFinder.get_nearest_object(blue_cups)
                nearest_yellow_cup = PathFinder.get_nearest_object(yellow_cups)

                target_point = TargetPoint(
                    PathFinder.calculate_center_point(nearest_yellow_cup.position, nearest_blue_cup.position))

                self.call_lower(target_point)
            else:
                self.call_lower(None)

    @staticmethod
    def calculate_center_point(position1: Tuple[float], position2: Tuple[float]) -> Tuple[float]:
        """
        calculates the center point between two points

        :param position1: point one
        :param position2: point two
        :return:
        """
        return ((position1[0] + position2[0]) / 2), ((position1[1] + position2[1]) / 2)

    @staticmethod
    def get_objects_by_type(detected_objects: List[DetectedObject], object_type: ObjectType) -> List[DetectedObject]:
        """
        reduce a list of detected objects by returning only detected objects of an specific ObjectType

        :param detected_objects: a list of all detected objects
        :param object_type: the ObjectType the list should be filtered with
        :return: a filtered list that contains only objects of the defined ObjectType
        """

        obj_list = []
        for obj in detected_objects:
            if obj.object_type == object_type:
                obj_list.append(obj)
        return obj_list

    @staticmethod
    def calculate_distance(detected_object: DetectedObject) -> float:
        """
        calculates the distance between a detected object and the car

        :param detected_object: the detected object
        :return: the distance between detected object and car
        """
        return math.sqrt(math.pow(detected_object.position[0], 2) + math.pow(detected_object.position[1], 2))

    @staticmethod
    def get_nearest_object(detected_objects: List[DetectedObject]) -> DetectedObject:
        """
        determines the closed object in relation to the car

        :param detected_objects: a list of all detected objects
        :return: returns the nearest object
        """
        nearest_object = min(detected_objects, key=lambda obj: PathFinder.calculate_distance(obj))
        return nearest_object

    def call_from_lower(self, message: str) -> None:
        print("ERROR: PathFinder: call_from_lower not implemented")
        raise NotImplementedError