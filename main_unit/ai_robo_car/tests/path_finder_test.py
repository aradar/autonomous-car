#!/usr/bin/env python3

import unittest

from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator, \
    DetectedObject
from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import ObjectType, TargetPoint
from ai_robo_car.layer.test_layer import TestLayer


class PathFinderTester(unittest.TestCase):
    def setUp(self):
        self.test_layer = TestLayer()
        self.path_finder = PathFinder(None, self.test_layer)

    @staticmethod
    def generate_sample_objects():
        sample_objects = [DetectedObject(tuple((2, 2)), 0.2, ObjectType.BLUE_CUP),
                          DetectedObject(tuple((2, 1)), 0.2, ObjectType.BLUE_CUP),
                          DetectedObject(tuple((2, 5)), 0.2, ObjectType.BLUE_CUP),
                          DetectedObject(tuple((1, 4)), 0.2, ObjectType.YELLOW_CUP),
                          DetectedObject(tuple((2, 0)), 0.2, ObjectType.YELLOW_CUP),
                          DetectedObject(tuple((2, 3)), 0.2, ObjectType.YELLOW_CUP),
                          DetectedObject(tuple((2, 4)), 0.2, ObjectType.UNDEFINED_OBJECT),
                          DetectedObject(tuple((4, 4)), 0.2, ObjectType.UNDEFINED_OBJECT),
                          DetectedObject(tuple((1, 4)), 0.2, ObjectType.UNDEFINED_OBJECT)]

        return sample_objects

    @staticmethod
    def generate_sample_objects_without_yellow():
        sample_objects = [DetectedObject(tuple((3, 0)), 0.2, ObjectType.BLUE_CUP),
                          DetectedObject(tuple((1, 4)), 0.2, ObjectType.UNDEFINED_OBJECT)]
        return sample_objects

    def test_all_valid(self):
        self.path_finder.call_from_upper(PathFinderTester.generate_sample_objects())
        self.assertEqual((2, 0.5), self.test_layer.message_from_upper.position)

    def test_yellow_missing(self):
        gen_objects = PathFinderTester.generate_sample_objects_without_yellow()
        self.path_finder.call_from_upper(gen_objects)
        self.assertEqual(None, self.test_layer.message_from_upper)


if __name__ == '__main__':
    unittest.main()
