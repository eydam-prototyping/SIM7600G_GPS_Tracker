from modem import ATCommand, Modem
from logging import Logging
import uasyncio

class ModemStateMachine:
    def __init__(self, modem):
        self.modem = modem
        self.state = "INIT"

    async def state_init(self):
        # Initialize the modem, set up UART, etc.
        Logging.info("State: INIT")
        #self.modem.power_cycle()
        self.state = "STARTUP"

    async def state_startup(self):
        # Send initial AT commands to wake up the modem and prepare it for registration
        Logging.info("State: STARTUP")
        for i in range(5):
            cmd = ATCommand("", _type="EXEC")
            self.modem.queue_command(cmd)
            await self.wait_for_command(cmd)
            if cmd.state == "FINISHED":
                self.state = "REGISTERING"
                return
        self.modem.power_cycle()
        self.state = "STARTUP"

    async def state_registering(self):
        # Send commands to register the modem on the network
        Logging.info("State: REGISTERING")
        cmd = ATCommand("+CREG", _type="READ")
        self.modem.queue_command(cmd)
        await self.wait_for_command(cmd)
        self.state = "WAIT"

    async def state_tracking(self):
        # Start tracking GPS or other data
        Logging.info("State: TRACKING")
        #self.modem.queue_command(ATCommand("+CGNSINF"))

    async def state_wait(self):
        # Wait for a condition or a certain amount of time
        Logging.info("State: WAIT")
        await uasyncio.sleep_ms(5000)
        self.state = "TRACKING"

    async def run_state_machine(self):
        while True:
            if self.state == "INIT":
                await self.state_init()
            elif self.state == "STARTUP":
                await self.state_startup()
            elif self.state == "REGISTERING":
                await self.state_registering()
            elif self.state == "TRACKING":
                await self.state_tracking()
            elif self.state == "WAIT":
                await self.state_wait()
            await uasyncio.sleep_ms(100)

    async def wait_for_command(self, command):
        while command.state != "FINISHED" and command.state != "FAILED":
            await uasyncio.sleep_ms(100)