from machine import UART, Pin
import uasyncio
import modem
from modemStateMachine import ModemStateMachine
sim7600g_uart = UART(1, baudrate=115200, tx=Pin(27), rx=Pin(26))
#sim7600g_uart.write("AT\r\n"); print(sim7600g_uart.read(-1))

sim7600g = modem.Modem(sim7600g_uart)
msm = ModemStateMachine(sim7600g)

async def main():
    sim7600g.run_in_background()
    await msm.run_state_machine()
    #
    #await uasyncio.sleep_ms(3000)
    #cmds.append(modem.ATCommand(""))
    #sim7600g.queue_command(cmds[-1])
    #while True:
    #    await uasyncio.sleep_ms(1000)
    #    print("Main loop")
    #    cmds.append(modem.ATCommand(""))
    #    sim7600g.queue_command(cmds[-1])

uasyncio.run(main())