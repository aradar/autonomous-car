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
