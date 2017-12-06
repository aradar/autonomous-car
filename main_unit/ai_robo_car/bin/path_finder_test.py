#!/usr/bin/env python3

import os
os.environ["PYTHONPATH"] = "../ai_robo_car/"

from ai_robo_car.layer import ObjectRecognizer, RelativeTranslator, PathFinder, PathTranslator, EngineCommunicator, DetectedObject
from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import ObjectType, TargetPoint

class PrintLayer(AbstractLayer[None, TargetPoint]):
    def call_from_upper(self, target_point: TargetPoint):
        print("target_point.position =", target_point.position[0], target_point.position[1])

def generate_sample_objects():
    sample_objects = []
    sample_objects.append(DetectedObject(tuple([2,2]), 0.2, ObjectType.BLUE_CUP))
    sample_objects.append(DetectedObject(tuple([4,3]), 0.2, ObjectType.BLUE_CUP))
    sample_objects.append(DetectedObject(tuple([2,1]), 0.2, ObjectType.BLUE_CUP)) # nearest
    sample_objects.append(DetectedObject(tuple([2,5]), 0.2, ObjectType.BLUE_CUP))
    sample_objects.append(DetectedObject(tuple([3,0]), 0.2, ObjectType.BLUE_CUP))
    sample_objects.append(DetectedObject(tuple([1,4]), 0.2, ObjectType.YELLOW_CUP))
    sample_objects.append(DetectedObject(tuple([2,1]), 0.2, ObjectType.YELLOW_CUP))
    sample_objects.append(DetectedObject(tuple([2,0]), 0.2, ObjectType.YELLOW_CUP)) # nearest
    sample_objects.append(DetectedObject(tuple([5,3]), 0.2, ObjectType.YELLOW_CUP))
    sample_objects.append(DetectedObject(tuple([2,3]), 0.2, ObjectType.YELLOW_CUP))
    sample_objects.append(DetectedObject(tuple([2,2]), 0.2, ObjectType.UNDEFINED_OBJECT))
    sample_objects.append(DetectedObject(tuple([1,3]), 0.2, ObjectType.UNDEFINED_OBJECT))
    sample_objects.append(DetectedObject(tuple([2,4]), 0.2, ObjectType.UNDEFINED_OBJECT))
    sample_objects.append(DetectedObject(tuple([4,4]), 0.2, ObjectType.UNDEFINED_OBJECT))
    sample_objects.append(DetectedObject(tuple([1,4]), 0.2, ObjectType.UNDEFINED_OBJECT))
    return sample_objects

def generate_sample_objects_without_yellow():
    sample_objects = []
    sample_objects.append(DetectedObject(tuple([3,0]), 0.2, ObjectType.BLUE_CUP))
    #sample_objects.append(DetectedObject(tuple([2,3]), 0.2, ObjectType.YELLOW_CUP))
    sample_objects.append(DetectedObject(tuple([1,4]), 0.2, ObjectType.UNDEFINED_OBJECT))
    return sample_objects

path_finder = PathFinder(None, PrintLayer(None, None))

detected_objects = generate_sample_objects()
path_finder.call_from_upper(detected_objects)

detected_objects = generate_sample_objects_without_yellow()
path_finder.call_from_upper(detected_objects)
