#!/usr/bin/env python3
import unittest

import time

from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator
from tests.engine_communicator_test import EngineCommunicatorServer


class LayerStackFunctionalityTester(unittest.TestCase):
    def setUp(self):
        self.object_recognizer = ObjectRecognizer(None, None)
        self.relative_translator = RelativeTranslator(None, None, camera_height=0.012, camera_position_angle=80,
                                                      camera_x_view_angle=150, camera_y_view_angle=94)
        self.path_finder = PathFinder(None, None)
        self.path_translator = PathTranslator(None, None)
        self.engine_communicator_server = EngineCommunicatorServer(-1)
        self.engine_communicator_server.start()
        self.engine_communicator = EngineCommunicator(None, None, True)

        self.create_layer_structure()

    def create_layer_structure(self):
        self.object_recognizer.lower = self.relative_translator
        self.relative_translator.lower = self.path_finder
        self.relative_translator.upper = self.object_recognizer
        self.path_finder.lower = self.path_translator
        self.path_finder.upper = self.relative_translator
        self.path_translator.lower = self.engine_communicator
        self.path_translator.upper = self.path_finder
        self.engine_communicator.upper = self.path_translator

    def test_layer_structure(self):
        for i in range(1000):
            self.object_recognizer.call_from_upper("")
            time.sleep(0.01)
            if len(self.engine_communicator_server.received_messages) > 0:
                print(self.engine_communicator_server.received_messages)
                self.engine_communicator_server.received_messages.clear()


if __name__ == '__main__':
    unittest.main()
