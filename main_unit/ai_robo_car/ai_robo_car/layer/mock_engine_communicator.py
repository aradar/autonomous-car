from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import EngineInstruction

class MockEngineCommunicator(AbstractLayer[EngineInstruction, str]):
    def call_from_upper(self, message: EngineInstruction) -> None:
        
        print("EngineCommunicator: call_from_upper -> speed:", message.speed, "steer:", message.steer)
        if self.lower is not None:
            self.call_lower(str("!"))

    def call_from_lower(self, message: str) -> None:
        print("EngineCommunicator: call_from_lower -> " + message)
        if self.upper is not None:
            self.upper.call_upper(message + str("!"))
