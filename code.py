import asyncio
import usb_cdc  # type: ignore
from core.command import Command
from core.startup import StartupService

serial = usb_cdc.console
command = Command(serial)

def setup():
    startup = StartupService()
    startup.exec_startup()

async def main_loop():
    setup()

    while True:
        await command.espera_comando()
        await asyncio.sleep(0.01)

asyncio.run(main_loop())