from typing import TypeVar, Generic

U = TypeVar("U")
L = TypeVar("L")


class AbstractLayer(Generic[U, L]):
    pass


class AbstractLayer(Generic[U, L]):
    def __init__(self, upper: AbstractLayer, lower: AbstractLayer):
        self.upper = upper
        self.lower = lower

    def call_from_lower(self, message: L) -> None:
        raise NotImplementedError

    def call_from_upper(self, message: U) -> None:
        raise NotImplementedError

    def call_lower(self, message: U) -> None:
        self.lower.call_from_upper(message)

    def call_upper(self, message: L) -> None:
        self.upper.call_from_lower(message)
