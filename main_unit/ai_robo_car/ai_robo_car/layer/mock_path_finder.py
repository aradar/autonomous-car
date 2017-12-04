from ai_robo_car.abstract_layer import AbstractLayer
from ai_robo_car.layer.data_objects import TargetPoint

class MockPathFinder(AbstractLayer[str, TargetPoint]):
    def call_from_upper(self, message: str) -> None:
        print("PathFinder: call_from_upper -> " + message)
        if self.lower is not None:
            self.call_lower(TargetPoint((0.5, 0.5)))

    def call_from_lower(self, message: str) -> None:
        print("PathFinder: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(message + str("!"))
