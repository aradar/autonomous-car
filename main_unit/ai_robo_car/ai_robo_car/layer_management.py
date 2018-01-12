import time
from enum import Enum
from multiprocessing.connection import Listener, Pipe
from threading import Thread, Event
from typing import Tuple, List, Union, Any

from multiprocessing import AuthenticationError

from ai_robo_car.abstract_layer import AbstractLayer


class RemoteControlCommand(Enum):
    """
    Enum that represents possible IPC commands.
    """

    SHUTDOWN = 1
    PAUSE = 2
    RESUME = 3


class RemoteControlMessage:
    """
    Wraps a RemoteControlCommand in a separate class which is than used for the IPC communication.
    """

    command: RemoteControlCommand

    def __init__(self, command: RemoteControlCommand) -> None:
        super().__init__()
        self.command = command


class ControllableThread(Thread):
    """
    A thread that can be paused or stopped through a Pipe which receives RemoteControlCommand objects.
    """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None,
                 command_pipe):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.command_pipe = command_pipe

    def read_new_command(self, use_timeout: bool = False, timeout: Union[float, None] = None) -> RemoteControlCommand:
        """
        Reads a command from the Pipe and returns it. If the pipe is empty and use_timeout is False than None gets
        returned.
        """
        command = None
        if use_timeout and self.command_pipe.poll(timeout):
            command: RemoteControlCommand = self.command_pipe.recv()
        elif self.command_pipe.poll():
            command: RemoteControlCommand = self.command_pipe.recv()
        return command

    def run(self):
        paused: bool = False
        while True:
            command = self.read_new_command(use_timeout=paused)

            if command == RemoteControlCommand.SHUTDOWN:
                return  # terminate the thread
            elif command == RemoteControlCommand.PAUSE:
                paused = True
            elif command == RemoteControlCommand.RESUME:
                paused = False

            if not paused:
                self.loop()

    def loop(self):
        """
        Is called like the body of a while loop from the thread itself and can be paused or stopped from it.

        This has to be implemented from subclasses otherwise a NotImplementedError gets raised!.
        """
        raise NotImplementedError("This function has to be implemented by subclasses!")


class PipeManager:
    """
    Helps with the creation and management of Pipe pairs.
    """

    pipe_pairs: List[Tuple[Any, Any]]

    def __init__(self) -> None:
        self.pipe_pairs = []

    def create_pipe_pair(self) -> Tuple[Any, Any]:
        """
        Creates a unidirectional pipe connection and returns the Connection objects. The first returned value is the
        receiver and the second the sender. Created pipe pairs get also added to a local storage to help the sender to
        message all pipes at once.
        """
        receiver, sender = Pipe(duplex=False)
        new_pair = (receiver, sender)
        self.pipe_pairs.append(new_pair)
        return new_pair

    def send_to_all(self, message) -> None:
        """
        Sends the given message to all pipe pairs.
        """
        for receiver, sender in self.pipe_pairs:
            sender.send(message)


class LayerManager(ControllableThread):
    """
    Manages the Layer structure through calling of the call_from_upper method on the object on top of the stack.
    """

    highest_layer: AbstractLayer
    heart_beat: Event

    def __init__(self, highest_layer: AbstractLayer, heart_beat: Event, command_pipe):
        super().__init__(command_pipe=command_pipe, name="LayerManagerThread")
        self.highest_layer = highest_layer
        self.heart_beat = heart_beat

    def loop(self):
        self.heart_beat.wait()
        self.highest_layer.call_from_upper("hallo")  # needs to be changed
        self.heart_beat.clear()


class RemoteControl(Thread):
    """
    Handles the incoming IPC communication and sends the commands to all other threads in the env.
    """

    address: Tuple[str, int]
    authkey: bytes
    pipe_manager: PipeManager

    def __init__(self, authkey: bytes, pipe_manager: PipeManager, address: Tuple[str, int] = ("localhost", 6789)):
        super().__init__(name="RemoteControlThread", daemon=True)
        self.authkey = authkey
        self.pipe_manager = pipe_manager
        self.address = address

    def run(self):
        try:
            with Listener(address=self.address, authkey=self.authkey) as listener:
                while True:
                    try:
                        with listener.accept() as connection:
                            message: RemoteControlMessage = connection.recv()
                            if isinstance(message, RemoteControlMessage):
                                self.pipe_manager.send_to_all(message.command)
                                if message.command == RemoteControlCommand.SHUTDOWN:
                                    return  # terminate this thread
                    except AuthenticationError:
                        pass
        except Exception:
            print("RemoteControlThread caught fire and terminates the whole application!")
            self.pipe_manager.send_to_all(RemoteControlCommand.SHUTDOWN)


class Heart(ControllableThread):
    """
    Produces a beat at the given frequency. Threads which want to listen to this beat have to wait for a change on the
    beat event object.
    """

    wait_time: float
    beat: Event

    def __init__(self, wait_time: float, command_pipe, heart_beat: Event):
        super().__init__(name="HeartThread", daemon=True, command_pipe=command_pipe)
        self.wait_time = wait_time
        self.beat = heart_beat

    def loop(self):
        time.sleep(self.wait_time)
        self.beat.set()


def build_and_start_env(highest_layer: AbstractLayer, ipc_secret: bytes, ipc_address: Tuple[str, int],
                        frequency: float = 30) -> None:
    """
    Constructs the env and starts it.
    """

    if frequency <= 0:
        raise ValueError("frequency is lower or equal than 0!")

    pipe_manger = PipeManager()
    remote_control = RemoteControl(pipe_manager=pipe_manger, authkey=ipc_secret, address=ipc_address)

    heart_beat = Event()
    receiver, _ = pipe_manger.create_pipe_pair()
    layer_manager = LayerManager(highest_layer=highest_layer, command_pipe=receiver, heart_beat=heart_beat)

    wait_time = 1 / frequency
    receiver, _ = pipe_manger.create_pipe_pair()
    heart = Heart(wait_time=wait_time, command_pipe=receiver, heart_beat=heart_beat)

    layer_manager.start()
    heart.start()
    remote_control.start()
