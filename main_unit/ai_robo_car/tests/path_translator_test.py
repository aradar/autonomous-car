#!/usr/bin/env python3

import unittest

from ai_robo_car.layer import PathTranslator
from ai_robo_car.layer.data_objects import TargetPoint, EngineInstruction
from ai_robo_car.layer.test_layer import TestLayer


class PathTranslatorTester(unittest.TestCase):

    def setUp(self):
        self.upper_test_layer = TestLayer()
        self.lower_test_layer = TestLayer()
        self.layer = PathTranslator(self.upper_test_layer, self.lower_test_layer)

    def tryHard(self, x, y, steer, speed):
        self.layer.call_from_upper(TargetPoint( (x, y) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, steer)
        self.assertEqual(detected_object.speed, speed)
        print("PathTranslator: call_from_upper -> x: %d, y: %d | call_lower -> steer: %d, speed: %d" % (x, y, steer, speed))

    def test_origin_coordinate(self):
        self.tryHard(0, 0, 0, 0)

    def test_invalid_negative_angle(self):
        self.tryHard(0, -1, 0, 0)

    def test_too_crank_angle(self):
        self.tryHard(1, 0, 45, 0.5)

    def test_normal_case_1(self):
        self.tryHard(0.5, 0.5, 45, 0.5)

    def test_normal_case_2(self):
        self.tryHard(0.9, 0.1, 45, 0.5)

    def test_normal_case_3(self):
        self.tryHard(0, 0.5, 0, 1.0)

    def test_normal_case_4(self):
        self.tryHard(-0.5, 0.5, -45, 0.5)

if __name__ == '__main__':
    unittest.main()
