import asyncio
import busio
import board

from utils.hardware import get_spi
from core.rtc import RTCService
from core.registro import RegistroService
from core.m90 import M90Service

async def show_help(cmd, serial):
    serial.write(f"Comandos disponibles:\n\r".encode())
    serial.write(f"ESC ?\n\r".encode())
    serial.write(f"ESC H - Setea fecha y hora en el RTC\n\r".encode())
    serial.write(f"ESC H - Lee fecha y hora desde el RTC\n\r".encode())
    serial.write(f"ESC R <num>,<total>\n\r".encode())
    serial.write(f"ESC M\n\r".encode())
    serial.write(f"ESC S\n\r".encode())

# async def run_iniciar_registro(cmd, serial, num, total):
#     cmd.data_logger = RegistroService(serial)
#     await cmd.data_logger.iniciar_registro(num, total)

# async def run_m90_start(cmd, serial):
#     if cmd.m90 is None:
#         spi = get_spi()
#         cmd.m90 = M90Service(serial, spi, board.D53, board.LED)
#     asyncio.create_task(cmd.m90.start_logging())
#     serial.write(b"Logging M90 iniciado.\r\n")

# async def run_m90_stop(cmd, serial):
#     if cmd.m90:
#         await cmd.m90.stop_logging()
#         serial.write(b"Logging M90 detenido.\r\n")
#     else:
#         serial.write(b"No hay logging activo.\r\n")

async def run_rtc_read(cmd, serial):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    ts = rtc.now()
    serial.write((RTCService.format(ts) + "\r\n").encode())

async def run_rtc_set(cmd, serial, yyyy, mm, dd, HH, MM, SS):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    y, mo, d, h, mi, s = map(int, (yyyy, mm, dd, HH, MM, SS))
    rtc.set_ymd_hms(y, mo, d, h, mi, s)
    serial.write(b"RTC OK\r\n")

COMANDOS = {
    "?": (show_help, 0),
    "H": (run_rtc_set, 6),              # Setear hora con 6 parámetros
    "h": (run_rtc_read, 0),             # Leer hora
    # "R": (run_iniciar_registro, 2),
    # "M": (run_m90_start, 0),
    # "S": (run_m90_stop, 0),
}