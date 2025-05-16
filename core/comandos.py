import asyncio
import busio
import board
from core.registro import Registro
from core.m90 import M90

async def show_help(cmd, serial):
    serial.write(f"Comandos disponibles:\n\r".encode())
    serial.write(f"ESC ?\n\r".encode())
    serial.write(f"ESC R <num>,<total>\n\r".encode())
    serial.write(f"ESC M\n\r".encode())
    serial.write(f"ESC S\n\r".encode())

async def run_iniciar_registro(cmd, serial, num, total):
    cmd.data_logger = Registro(serial)
    await cmd.data_logger.iniciar_registro(num, total)

async def run_m90_start(cmd, serial):
    if not hasattr(cmd, "m90"):
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        while not spi.try_lock():
            pass
        spi.configure(baudrate=500000, phase=0, polarity=0)
        cmd.m90 = M90(serial, spi, board.D53, board.LED)

    asyncio.create_task(cmd.m90.start_logging())

async def run_m90_stop(cmd, serial):
    if hasattr(cmd, "m90"):
        await cmd.m90.stop_logging()
        serial.write(b"Logging M90 detenido.\n\r")

COMANDOS = {
    "?": (show_help, 0),
    "R": (run_iniciar_registro, 2),
    "M": (run_m90_start, 0),
    "S": (run_m90_stop, 0),
}