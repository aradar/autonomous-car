from ai_robo_car.abstract_layer import AbstractLayer


class RelativeTranslator(AbstractLayer[str, str]):

    def call_from_upper(self, message: str) -> None:
        print("RelativeTranslator: call_from_upper -> " + message)
        if self.lower is not None:
            self.lower.call_from_upper(message + str("!"))

    def call_from_lower(self, message: str) -> None:
        print("RelativeTranslator: call_from_lower -> " + message)
        if self.upper is not None:
            self.upper.call_from_lower(message + str("!"))
