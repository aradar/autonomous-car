#!/usr/bin/env python3
import unittest

import _thread
import struct
import os
import socket
import math
from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator
from ai_robo_car.layer.data_objects import EngineInstruction 


class EngineCommunicatorTester(unittest.TestCase):
    def setUp(self):
        self.sample_objects = []
        self.sample_objects.append(EngineInstruction(-1, -30))
        self.sample_objects.append(EngineInstruction(1, -30))
        self.sample_objects.append(EngineInstruction(-1, 30))
        self.sample_objects.append(EngineInstruction(1, 30))
        self.server_socket = self.setup_server()
        self.layer = EngineCommunicator(None, None, True)

    def setup_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (("127.0.0.1", 8000))
        server_socket.bind(addr)
        server_socket.listen(1)
        _thread.start_new_thread(self.handler,())
        return server_socket

    def handler(self):
        (client,addr) = self.server_socket.accept()
        self.recvd_msgs = []
        samples_len = len(self.sample_objects)
        for i in range(samples_len):
            result = struct.unpack("<Bff", client.recv(9))
            self.recvd_msgs.append(result)

    def test_engine_communicator_received_data_should_be_ok(self):
        for sample_object in self.sample_objects:
            self.layer.call_from_upper(sample_object)

        while(len(self.recvd_msgs) < len(self.sample_objects)):
            pass

        for i, sample_object in enumerate(self.sample_objects):
            self.assertEqual((i*64, math.fabs(sample_object.steer), math.fabs(sample_object.speed)), self.recvd_msgs[i], msg=i)
    
    def tearDown(self):
        self.layer.close()
        self.server_socket.close()

if __name__ == '__main__':
    unittest.main()
