#!/usr/bin/env python3

import unittest

from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator, DetectedObject
from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.test_layer import TestLayer


class ObjectRecognizerTester(unittest.TestCase):
    def setUp(self):
        test_layer = TestLayer()
        self.object_recognizer = ObjectRecognizer(None, None)
    
    def test_all_valid(self):
        self.object_recognizer.call_from_upper(None)

if __name__ == '__main__':
    unittest.main()
