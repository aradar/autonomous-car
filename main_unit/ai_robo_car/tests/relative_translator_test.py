#!/usr/bin/env python3

import unittest

from ai_robo_car.layer import RelativeTranslator
from ai_robo_car.layer.data_objects import BoundingBox, ObjectType
from ai_robo_car.layer.test_layer import TestLayer


class RelativeTranslatorTester(unittest.TestCase):

    def setUp(self):
        self.upper_test_layer = TestLayer()
        self.lower_test_layer = TestLayer()
        self.layer = RelativeTranslator(self.upper_test_layer, self.lower_test_layer, 0.1, 80, 150, 94)

    def test_coordinate_translation_should_be_ok(self):
        bounding_box = BoundingBox(0.418, 0.582, 0.55, 0.9, 0.164, 0.35, ObjectType.BLUE_CUP)
        self.layer.call_from_upper([bounding_box])
        detected_object = self.lower_test_layer.message_from_upper[0]
        self.assertEqual(detected_object.radius, bounding_box.width / 2)
        self.assertAlmostEqual(detected_object.position[0], 0.0, 3)
        self.assertAlmostEqual(detected_object.position[1], 0.173, 3)


if __name__ == '__main__':
    unittest.main()
