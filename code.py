import asyncio
from core.startup import StartupService
from utils.hardware import serial_task, wifi_task
from core.command import Command
from core.wifi import get_wifi


cmd = Command()
wifi = get_wifi()

def setup():
    startup = StartupService()
    startup.exec_startup()

async def main_loop():
    setup()

    asyncio.create_task(serial_task(cmd))
    asyncio.create_task(wifi_task(cmd, wifi))

    while True:
        # await command.espera_comando()
        await asyncio.sleep(0.01)

asyncio.run(main_loop())