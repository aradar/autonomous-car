import threading
import time
from enum import Enum
from multiprocessing.connection import Listener
from threading import Thread, Event
from typing import Tuple

from ai_robo_car.abstract_layer import AbstractLayer


class StoppableThread(Thread):
    pass


class Heart(StoppableThread):
    pass


class Manager:
    pass


class RemoteControl(StoppableThread):
    pass


class ManagerContext:
    """
    Represents the threading context of the layer_manager module.
    """

    heart: Heart
    manager: Manager
    remoteControl: RemoteControl

    def __init__(self, heart: Heart, manager: Manager, remote_control: RemoteControl) -> None:
        super().__init__()
        self.remoteControl = remote_control
        self.manager = manager
        self.heart = heart
        self.remoteControl = remote_control


class RemoteControlCommand(Enum):
    """
    Enum which represents the commands which are possible for the IPC.
    """

    SHUTDOWN = 1
    PAUSE = 2
    RESUME = 3


class RemoteControlMessage:
    """
    Wrapper class for a command. The message than is send through a ipc socket and allows the remote control of server.
    """

    command: RemoteControlCommand

    def __init__(self, command: RemoteControlCommand) -> None:
        super().__init__()
        self.command = command


class StoppableThread(Thread):
    """
    Extension of the default Thread class which allows the stopping or pausing and resuming of threads if implemented
    accordingly.

    If you want to handle pausing and resuming you have to check the resume_event and paused variable.
    If you want to handle stopping of a thread you have to check the stop_event.
    """

    stop_event: Event
    resume_event: Event
    paused: bool = False

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.stop_event = Event()
        self.resume_event = Event()

    def stop(self):
        """
        Stops the thread and waits for its termination.
        """
        self.stop_event.set()
        self.resume()
        Thread.join(self)

    def pause(self):
        """
        Pauses the thread.
        """
        self.paused = True

    def resume(self):
        """
        Resumes the thread.
        """
        self.paused = False
        self.resume_event.set()


class Manager:
    """
    Handles the construction of the environment to manage the AbstractLayer stack. This is the only class besides
    RemoteControlMessage which should get instantiated outside of the module.
    """

    highest_layer: AbstractLayer
    stop_event: Event
    frequency: float
    context: ManagerContext

    def __init__(self, highest_layer: AbstractLayer, ipc_secret: str, ipc_address: Tuple[str, int],
                 frequency: float = 30):
        """
        :param highest_layer: the layer of the structure which has the upper variable set to None
        :param ipc_secret: secret which gets used for the encryption of ipc the communication
        :param ipc_address: address at which the ipc socket listens
        :param frequency: frequency at which the logic loop runs
        """
        if frequency <= 0:
            raise ValueError("frequency is lower or equal than 0!")

        self.frequency = frequency
        self.highest_layer = highest_layer
        self.ipc_address = ipc_address
        self.ipc_secret = ipc_secret
        self.stop_event = Event()
        self.context = None

    def start(self):
        """
        Constructs the env and starts the work of the AbstractLayer structure on the mainthread.
        """
        wait_time = 1 / self.frequency
        heart = Heart(wait_time=wait_time)
        remote_control = RemoteControl(authkey=self.ipc_secret, address=self.ipc_address)

        self.context = ManagerContext(heart=heart, manager=self, remote_control=remote_control)
        heart.context = self.context
        remote_control.context = self.context

        heart.start()
        remote_control.start()
        self.run()

    def stop(self):
        """
        Stops the work on the thread and waits for its termination.
        """
        self.stop_event.set()
        Thread.join(threading.main_thread())

    def run(self):
        """
        Main function of the mainthread.
        """
        while not self.stop_event.is_set():
            try:
                self.context.heart.beat.wait()
                self.highest_layer.call_from_upper("hallo")  # needs to be changed
                self.context.heart.beat.clear()
            except KeyboardInterrupt:
                self.context.heart.stop()
                self.context.remoteControl.stop()

    def call_from_upper(self, message: None) -> None:
        raise NotImplementedError("this layer does not support messages from other layers!")

    def call_from_lower(self, message: None) -> None:
        raise NotImplementedError("this layer does not support messages from other layers!")


class RemoteControl(StoppableThread):
    """
    Handles the incoming ipc communication and sends information to the other threads in the current context.

    Calling a stop if the env pauses causes a deadlock. We should probably fix this :'(
    """

    address: Tuple[str, int]
    authkey: str
    context: ManagerContext

    def __init__(self, authkey: str, address: Tuple[str, int] = ("localhost", 6789)):
        super().__init__(name="RemoteControlThread", daemon=True)
        self.authkey = authkey
        self.address = address
        self.context = None

    def run(self):
        try:
            with Listener(address=self.address, authkey=self.authkey.encode()) as listener:
                while not self.stop_event.is_set():
                    with listener.accept() as connection:
                        message: RemoteControlMessage = connection.recv()
                        if isinstance(message, RemoteControlMessage):
                            if message.command is RemoteControlCommand.SHUTDOWN:
                                self.context.heart.stop()
                                self.context.manager.stop()
                                return
                            elif message.command is RemoteControlCommand.PAUSE:
                                self.context.heart.pause()
                            elif message.command is RemoteControlCommand.RESUME:
                                self.context.heart.resume()
        except Exception:
            print("RemoteControlThread caught fire and terminates the whole application!")
            self.context.heart.stop()
            self.context.manager.stop()


class Heart(StoppableThread):
    """
    Produces a beat at the given frequency. Threads which want to listen to this beat have to wait for a change on the
    beat event object.
    """

    wait_time: float
    beat: Event
    context: ManagerContext

    def __init__(self, wait_time: float):
        super().__init__(name="HeartThread", daemon=True)
        self.wait_time = wait_time
        self.beat = Event()
        self.context = None

    def stop(self):
        self.stop_event.set()
        Thread.join(self)

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(self.wait_time)
            self.beat.set()

            if self.paused:
                self.resume_event.wait()
                self.resume_event.clear()
