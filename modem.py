import uasyncio
import uselect
from machine import Pin
import utime
from logging import Logging

class ATCommand:
    def __init__(self, _cmd:str, _type:str, _param:str=None, _data:str=None, timeout:int=1000):
        self.cmd = _cmd
        self.type = _type
        self.param = _param
        self.data = _data
        self.state = "INIT"
        self.timeout = timeout

    def _receive_handler(self, data):
        # Process the received data and update the state based on the responses
        Logging.info(f"Received data: {data}")
        for line in data.split("\n"):
            if line.strip() in ["OK"]:
                self.state = "FINISHED"
            elif line.strip() in ["ERROR"]:
                self.state = "FAILED"

    def to_string(self):
        # Convert the AT command to a string representation
        if self.type == "TEST":
            return "AT" + self.cmd + "=?\r\n"
        elif self.type == "READ":
            return "AT" + self.cmd + "?\r\n"
        elif self.type == "WRITE":
            return "AT" + self.cmd + "=" + self.param + "\r\n"
        elif self.type == "EXEC":
            return "AT" + self.cmd + "\r\n"

class Modem:
    def __init__(self, uart, pwr_key=4):
        self.uart = uart
        self._poll = uselect.poll()
        self._poll.register(uart, uselect.POLLIN)
        self.pwr_key = Pin(pwr_key, Pin.OUT)
        self.current_command = None
        self.command_queue = []

    def power_cycle(self):
        # Power cycle the modem by toggling the power key
        self.pwr_key.value(1)
        utime.sleep_ms(2000)
        self.pwr_key.value(0)

    def queue_command(self, command):
        # Add an AT command to the queue
        self.command_queue.append(command)

    def _send_at_command(self, command):
        # Send an AT command to the modem
        Logging.info(f"Sending command: {command.to_string().strip()}")
        self.current_command = command
        self.uart.write(command.to_string())
        self.state = "RUNNING"
    
    async def run_in_background_task(self):
        Logging.info("Starting background task")
        t0 = utime.ticks_ms()
        while True:
            if self.current_command is not None and utime.ticks_diff(utime.ticks_ms(), t0) > self.current_command.timeout:
                # If the current command has timed out, mark it as failed
                self.current_command.state = "TIMEOUT"
                self.current_command = None
            await uasyncio.sleep_ms(100)
            events = self._poll.poll(100)
            for event in events:
                # Handle the received events (data from the serial interface)
                Logging.info("Event received")
                data = event[0].read().decode()
                if self.current_command is not None:
                    # If there is a current command, process the received data
                    self.current_command._receive_handler(data)
                    if self.current_command.state in ["FINISHED", "FAILED"]:
                        self.current_command = None
                Logging.info(data)
            # If no current command is being processed, get the next one from the queue
            if self.current_command is None:
                if len(self.command_queue) > 0:
                    self._send_at_command(self.command_queue.pop(0))
                    t0 = utime.ticks_ms()

    def run_in_background(self):
        Logging.info("Starting background task")
        # Start the background task
        t = uasyncio.create_task(self.run_in_background_task())
        return t
