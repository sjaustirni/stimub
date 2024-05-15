import socket
import time
from datetime import datetime
from enum import Enum, auto
from daqmx import NIDAQmxInstrument


class BaseInput:
    def connect(self) -> None:
        pass

    def wait_for_trigger(self) -> bool:
        pass


class TCPInput(BaseInput):
    """
    Read a string-based TCP packet and trigger on the specified label.
    """
    def __init__(self, tcp_ip: str, tcp_port: int, trigger_label: str):
        """
        :param tcp_ip:  TCP server IP
        :param tcp_port: TCP server port
        :param trigger_label: Case-sensitive label that will trigger a stimulation.
        """
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.trigger_label = trigger_label
        self.socket = None

    def connect(self) -> None:
        """
        Establishes a TCP connection with the server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.tcp_ip, self.tcp_port))
        print(self.socket)

    def wait_for_trigger(self) -> bool:
        """
        Blocking function to wait for a TCP message.
        :return: `True` if the message is the trigger label, otherwise it continues waiting. `False` if connection is closed.
        """
        BUFFER_SIZE = 1024

        while True:
            data = self.socket.recv(BUFFER_SIZE)
            if not data:
                break
            text_label = data.decode().strip()

            if text_label == self.trigger_label:
                return True

        return False

class ConsoleInput(BaseInput):
    """
    Reads console input and sends a trigger on Enter. Useful for testing.
    """
    def wait_for_trigger(self) -> bool:
        """
        Blocking function until user types Enter into the console.
        :return: Always `True`
        """
        print("\nHit Enter to trigger: ", end="")
        input()
        return True


class BaseTrigger:
    def stimulate(self):
        pass


class ConsoleTrigger(BaseTrigger):
    """
    Sends a message on trigger. Useful for testing.
    """
    def stimulate(self) -> None:
        print("Console Stimulation")


class NiDAQTrigger(BaseTrigger):
    """
    Sends a NiDAQ stimulation on trigger.
    """
    def __init__(self, voltage: float, pulse_width_s: float, pause_width_s: float, n_pulses: int):
        """
        :param voltage: Sets the stimulation voltage, in volts.
        :param pulse_width_s: Length of a single pulse in stimulation in seconds.
        :param pause_width_s:  Length of a pause between pulses in seconds.
        :param n_pulses: Number of pulses in a stimulation.
        """
        self.voltage = voltage
        self.pulse_width = pulse_width_s
        self.pause_width = pause_width_s
        self.n_pulses = n_pulses

        self.daq = NIDAQmxInstrument()

    def stimulate(self):
        print("NiDAQ stimulation")
        for i in range(self.n_pulses):
            print("Start: ", datetime.now().strftime("%H:%M:%S.%f")[:-3], end="")
            self.daq.ao0 = self.voltage
            time.sleep(self.pulse_width)

            print(" End: ", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            self.daq.ao0 = 0
            time.sleep(self.pause_width)


class Proxy:
    """
    Establishes a connection between input and stimulation device.
    """
    def __init__(self, input_obj: BaseInput, trigger: BaseTrigger, seconds_between_stimulations: int = 5):
        """
        :param input_obj: Input object that sends a message at the time of wanted stimulation.
        :param trigger: Trigger object that triggers the stimulation device.
        :param seconds_between_stimulations: Sliding window length in seconds in which only the first stimulation is triggered. The consecutive ones are ignored.
        """
        self.input = input_obj
        self.trigger = trigger
        self.seconds_between_stimulations = seconds_between_stimulations

    def start(self) -> None:
        """
        Starts the proxy server. After the proxy server has started and connection to both input and stimulation device
        are established, stimulations can be triggered.
        """
        self.input.connect()
        last_stimulation_time = 0

        while True:
            triggered = self.input.wait_for_trigger()

            if triggered:
                current_time = time.time()
                if (current_time - last_stimulation_time) < self.seconds_between_stimulations:
                    print("Stimulation prevented from firing")
                    continue
                last_stimulation_time = time.time()
                self.trigger.stimulate()
