#!/usr/bin/env python3
import _thread
import math
import socket
import struct
import unittest

import time

from ai_robo_car.layer import EngineCommunicator
from ai_robo_car.layer.data_objects import EngineInstruction


class EngineCommunicatorServer:
    def __init__(self, receive_size):
        self.received_messages = []
        self.address = ("127.0.0.1", 8000)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_size = receive_size

    def start(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(1)
        _thread.start_new_thread(self.handler, ())
        return self.server_socket

    def handler(self):
        (client, address) = self.server_socket.accept()
        received_size = 0
        while self.receive_size is -1 or self.receive_size >= received_size:
            result = struct.unpack("<Bff", client.recv(9))
            received_size = received_size + 1
            self.received_messages.append(result)
            time.sleep(0.001) # otherwise the server throws a unhandled exception


class EngineCommunicatorTester(unittest.TestCase):
    def setUp(self):
        self.sample_objects = []
        self.sample_objects.append(EngineInstruction(-1, -30))
        self.sample_objects.append(EngineInstruction(1, -30))
        self.sample_objects.append(EngineInstruction(-1, 30))
        self.sample_objects.append(EngineInstruction(1, 30))
        self.engine_communication_server = EngineCommunicatorServer(len(self.sample_objects))
        self.server_socket = self.engine_communication_server.start()
        self.layer = EngineCommunicator(None, None, True)

    def test_engine_communicator_received_data_should_be_ok(self):
        for sample_object in self.sample_objects:
            self.layer.call_from_upper(sample_object)

        while len(self.engine_communication_server.received_messages) < len(self.sample_objects):
            pass

        for i, sample_object in enumerate(self.sample_objects):
            self.assertEqual((i * 64, math.fabs(sample_object.steer), math.fabs(sample_object.speed)),
                             self.engine_communication_server.received_messages[i], msg=i)

    def tearDown(self):
        self.layer.close()
        self.server_socket.close()


if __name__ == '__main__':
    unittest.main()
