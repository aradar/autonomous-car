#!/usr/bin/env python3
import struct
import os
import _thread
from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator
from ai_robo_car.layer.data_objects import EngineInstruction 

import socket

msg_recvd = False

def handler(socket):
    (client,addr) = socket.accept()
    print(struct.unpack("<Bff", client.recv(1024)))
    global msg_recvd
    socket.close()
    msg_recvd = True

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = (("127.0.0.1", 8000))
socket.bind(addr)
socket.listen(1)

_thread.start_new_thread( handler, (socket, ) )
engine_communicator = EngineCommunicator(None, None, True)

engine_instruction = EngineInstruction(1, 30)
engine_communicator.call_from_upper(engine_instruction)

while(not msg_recvd):
    pass
