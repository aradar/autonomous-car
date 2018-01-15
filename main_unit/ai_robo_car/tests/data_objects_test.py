#!/usr/bin/env python3

import unittest

from ai_robo_car.layer.data_objects import *

class PathTranslatorTester(unittest.TestCase):
    def test_bounding_box_str(self):
        obj = BoundingBox(0, 1, 2, 3, 4, 5, ObjectType.BLUE_CUP)
        self.assertEqual(str(obj),
                "BoundingBox: left 0, right 1, top 2, bottom 3, width 4, height 5, object_type {}".format(ObjectType.BLUE_CUP))

    def test_detected_object_str(self):
        obj = DetectedObject((0, 1), 2, ObjectType.BLUE_CUP)
        self.assertEqual(str(obj),
                "DetectedObject: position (0, 1), radius 2, objects_type {}".format(ObjectType.BLUE_CUP))

    def test_target_point_str(self):
        obj = TargetPoint((0, 1))
        self.assertEqual(str(obj),
                "TargetPoint: position (0, 1)")

    def test_engine_instruction_str(self):
        obj = EngineInstruction(0, 1)
        self.assertEqual(str(obj),
                "EngineInstruction: speed 0, steer 1")

if __name__ == '__main__':
    unittest.main()
