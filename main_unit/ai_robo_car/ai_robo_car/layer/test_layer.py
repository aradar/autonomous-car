from ai_robo_car.abstract_layer import AbstractLayer


class TestLayer(AbstractLayer):

    def __init__(self):
        super().__init__(None, None)

    def call_from_upper(self, message) -> None:
        self.message_from_upper = message

    def call_from_lower(self, message) -> None:
        self.message_from_lower = message
