from typing import TypeVar, Generic

U = TypeVar("U")
L = TypeVar("L")


class AbstractLayer(Generic[U, L]):
    pass


class AbstractLayer(Generic[U, L]):
    """
    Abstract class which is the base of the layer structure. All layers should extend this class and implement the
    call_from_lower and call_from_upper methods. If one of those methods can't be implemented a NotImplementedError
    should be raised.

    The generic type U represents the message object of the upper layer and L the one of the lower.
    """
    def __init__(self, upper: AbstractLayer, lower: AbstractLayer):
        """
        :param upper: the layer above this instance of the AbstractLayer
        :param lower: the layer below this instance of the AbstractLayer
        """

        self.upper = upper
        self.lower = lower

    def call_from_lower(self, message: L) -> None:
        """
        Gets called if the lower layer sends a message.

        :param message: received message
        """

        raise NotImplementedError

    def call_from_upper(self, message: U) -> None:
        """
        Gets called if the higher layer sends a message.

        :param message: received message
        """

        raise NotImplementedError

    def call_lower(self, message: U) -> None:
        """
        Calls the layer below with the given message.

        :param message: message to be send
        """

        self.lower.call_from_upper(message)

    def call_upper(self, message: L) -> None:
        """
        Calls the layer above with the given message.

        :param message: message to be send
        """

        self.upper.call_from_lower(message)

    def stop(self) -> None:
        """
        Gets called if the complete layer structure is about to shutdown. Methods which have resources should do there
        clean up in this function.
        """
        pass

    def pause(self) -> None:
        """
        Gets called if the layer structure pauses. This is primarily for the EngineCommunicator to stop it from driving
        against a wall.
        """
        pass

    def resume(self) -> None:
        """
        Gets called if the layer structure resumes its work after being paused.
        """
        pass
