#!/usr/bin/env python3

import send
import fileinput

drive = 50
steer = 50

drive_acc = 5;
steer_acc = 5;

while (True):
    for line in fileinput.input():
        if (line == 'a'):
            steer = steer - steer_acc;
        else if (line == 'd'):
            steer = steer + steer_acc;
        else if (line == 'w'):
            drive = drive + drive_acc;
        else if (line == 's'):
            drive = drive - drive_acc;

        if (drive < 50):
            os.system("./send.py +d " + drive + " 0");
        os.system("./send.py +s " + steer + " 0");
