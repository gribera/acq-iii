import time
import usb_cdc # type: ignore
from core.command import Command

# Configuración del puerto serial
serial = usb_cdc.console

command = Command(serial)

while True:
    command.espera_comando()
    time.sleep(0.1)