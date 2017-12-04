from ai_robo_car.abstract_layer import AbstractLayer


class PathFinder(AbstractLayer[str, str]):
    def call_from_upper(self, message: str) -> None:
        print("PathFinder: call_from_upper -> " + message)
        if self.lower is not None:
            self.call_lower(message + str("!"))

    def call_from_lower(self, message: str) -> None:
        print("PathFinder: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(message + str("!"))
