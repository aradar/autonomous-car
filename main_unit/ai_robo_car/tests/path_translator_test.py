import unittest

from ai_robo_car.layer import PathTranslator
from ai_robo_car.layer.data_objects import TargetPoint, EngineInstruction
from ai_robo_car.layer.test_layer import TestLayer


class PathTranslatorTester(unittest.TestCase):

    def setUp(self):
        self.upper_test_layer = TestLayer()
        self.lower_test_layer = TestLayer()
        self.layer = PathTranslator(self.upper_test_layer, self.lower_test_layer)

    def test_origin_coordinate(self):
        self.layer.call_from_upper(TargetPoint( (0, 0) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 0)
        self.assertEqual(detected_object.speed, 0)

    def test_invalid_negative_angle(self):
        self.layer.call_from_upper(TargetPoint( (0, -1) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 0)
        self.assertEqual(detected_object.speed, 0)

    def test_too_crank_angle(self):
        self.layer.call_from_upper(TargetPoint( (1, 0) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 45)
        self.assertEqual(detected_object.speed, 0.5)

    def test_normal_case_1(self):
        self.layer.call_from_upper(TargetPoint( (0.5, 0.5) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 45)
        self.assertEqual(detected_object.speed, 0.5)

    def test_normal_case_2(self):
        self.layer.call_from_upper(TargetPoint( (0.9, 0.1) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 45)
        self.assertEqual(detected_object.speed, 0.5)

    def test_normal_case_3(self):
        self.layer.call_from_upper(TargetPoint( (0, 0.5) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, 0)
        self.assertEqual(detected_object.speed, 1.0)

    def test_normal_case_4(self):
        self.layer.call_from_upper(TargetPoint( (-0.5, 0.5) ))
        detected_object = self.lower_test_layer.message_from_upper
        self.assertEqual(detected_object.steer, -45)
        self.assertEqual(detected_object.speed, 0.5)

if __name__ == '__main__':
    unittest.main()
