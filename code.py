import asyncio
import usb_cdc  # type: ignore
from core.command import Command

serial = usb_cdc.console
command = Command(serial)

async def main_loop():
    while True:
        await command.espera_comando()
        await asyncio.sleep(0.01)

asyncio.run(main_loop())