import asyncio
import busio
import board

from core.rtc import RTCService
from core.registro import Registro
from core.m90 import M90

async def show_help(cmd, serial):
    serial.write(f"Comandos disponibles:\n\r".encode())
    serial.write(f"ESC ?\n\r".encode())
    serial.write(f"ESC H - Setea fecha y hora en el RTC\n\r".encode())
    serial.write(f"ESC H - Lee fecha y hora desde el RTC\n\r".encode())
    serial.write(f"ESC R <num>,<total>\n\r".encode())
    serial.write(f"ESC M\n\r".encode())
    serial.write(f"ESC S\n\r".encode())


async def run_iniciar_registro(cmd, serial, num, total):
    cmd.data_logger = Registro(serial)
    await cmd.data_logger.iniciar_registro(num, total)

async def run_m90_start(cmd, serial):
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    while not spi.try_lock():
        pass
    spi.configure(baudrate=500000, phase=0, polarity=0)
    cmd.m90 = M90(serial, spi, board.D53, board.LED)

    asyncio.create_task(cmd.m90.start_logging())

async def run_m90_stop(cmd, serial):
    await cmd.m90.stop_logging()
    serial.write(b"Logging M90 detenido.\n\r")

async def run_rtc_read(cmd, serial):
    rtc = RTCService()
    ts = rtc.now()
    serial.write((RTCService.format(ts) + "\r\n").encode())

async def run_rtc_set(cmd, serial, yyyy, mm, dd, HH, MM, SS):
    try:
        y = int(yyyy); mo = int(mm); d = int(dd)
        h = int(HH); mi = int(MM); s = int(SS)
        rtc = RTCService()

        rtc.set_ymd_hms(y, mo, d, h, mi, s)
        serial.write(b"RTC OK\r\n")
    except Exception as e:
        serial.write((f"RTC ERR: {e}\r\n").encode())

COMANDOS = {
    "?": (show_help, 0),
    "H": (run_rtc_set, 6),              # Setear hora con 6 parámetros
    "h": (run_rtc_read, 0),             # Leer hora
    "R": (run_iniciar_registro, 2),
    "M": (run_m90_start, 0),
    "S": (run_m90_stop, 0),
}