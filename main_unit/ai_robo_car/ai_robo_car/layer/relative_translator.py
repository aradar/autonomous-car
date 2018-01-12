from math import tan, isclose, radians
from typing import List, Tuple

from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import BoundingBox, DetectedObject


class RelativeTranslator(AbstractLayer[List[BoundingBox], List[DetectedObject]]):
    """
    This layer translates the absolute coordinates from the given bounding boxes into relative coordinates based on
    the camera position. The unit used in the coordinate system is defined by the camera_height variable. The next
    layer gets an DetectedObject for each given BoundingBox object. Those contain the object type as well as their
    position and radius.
    """

    def __init__(self, upper: AbstractLayer, lower: AbstractLayer, camera_height: float, camera_position_angle: float,
                 camera_x_view_angle: float, camera_y_view_angle: float,
                 original_image_aspect_ratio: Tuple[float, float] = (1.6, 1.)):
        """
        The original_image_aspect_ratio variable is optional and defaults to (1.6, 1.)

        The unit of measure of the camera_height Variable defines the unit of measure which results from this layer!

        :param upper: the layer above (normally ObjectRecognizer) this instance of the RelativeTranslator
        :param lower: the layer below (normally PathFinder) this instance of the RelativeTranslator
        :param camera_height: the height at which the camera is mounted preferably in meters
        :param camera_position_angle: the angle in degrees at which the camera is mounted
        :param camera_x_view_angle: the horizontal view angle in degrees of the camera
        :param camera_y_view_angle: the vertical view angle in degrees of the camera
        :param original_image_aspect_ratio: the aspect ratio of the original footage
        """

        super().__init__(upper, lower)

        self.camera_height = camera_height
        self.camera_position_angle = camera_position_angle
        self.camera_x_view_angle = camera_x_view_angle
        self.camera_y_view_angle = camera_y_view_angle
        self.original_image_aspect_ratio = original_image_aspect_ratio

    def call_from_upper(self, bounding_boxes: List[BoundingBox]) -> None:
        if self.lower is not None:
            if bounding_boxes is None:
                self.call_lower(None)
                return

            detected_objects = []
            for bounding_box in bounding_boxes:
                if self.proportions_fit(bounding_box.width, bounding_box.height):
                    radius = bounding_box.width * 0.5
                    y = self.calc_y(bounding_box.bottom, radius)
                    x = self.calc_x(bounding_box.left, radius, y)
                    detected_objects.append(DetectedObject((x, y), radius, bounding_box.object_type))

            if len(detected_objects) == 0:
                detected_objects = None

            self.call_lower(detected_objects)

    def call_from_lower(self, message: str) -> None:
        raise NotImplementedError

    def proportions_fit(self, width: float, height: float, allowed_variance: float = 0.1) -> bool:
        """
        Checks if the proportions of the detected object fit those of a real cup.

        :param width: width of the object
        :param height: height of the object
        :param allowed_variance: allowed variance for the discrepancy from the real size of the cup
        :return: if proportion of the object is in the allowed_variance range
        """

        cup_proportion = 6.0 / 8.0   # width / height in cm, correct ratio would be 7.0 / 8.0
        object_proportion = width * self.original_image_aspect_ratio[0] / height * self.original_image_aspect_ratio[1]
        return isclose(cup_proportion, object_proportion, abs_tol=allowed_variance)

    def calc_x(self, x_absolute_left: float, radius: float, y_relative: float) -> float:
        """
        Calculates the horizontal distance from camera to the center of the object and returns it in a coordinate
        system based on the position of the camera.

        :param x_absolute_left: left x value of the bounding box of the object
        :param radius: radius of the object
        :param y_relative: previously calculated y value of the camera coordinate system
        :return: horizontal distance to the object
        """

        beta = self.camera_x_view_angle
        gamma = (x_absolute_left + radius) * beta - beta * 0.5
        return tan(radians(gamma)) * y_relative

    def calc_y(self, y_absolute_bottom: float, radius: float) -> float:
        """
        Calculates the forward distance from camera to the center of the object and returns it in a coordinate system based
        on the position of the camera.

        :param radius: radius of the object
        :param y_absolute_bottom: bottom y value of the bounding box of the object
        :return: forward distance to the object
        """

        alpha = self.camera_position_angle
        beta = self.camera_y_view_angle
        gamma = alpha - (y_absolute_bottom * beta - beta * 0.5)
        return tan(radians(gamma)) * self.camera_height + radius
