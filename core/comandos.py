import asyncio
import busio
import board

from utils.help import show_help, show_version
from core.startup import StartupService
from core.rtc import RTCService
from core.wifi import get_wifi

from config import (MEMORIAS, EQUIPO, VERSION, FECHA)

async def get_help(cmd, serial):
    show_help()

async def get_version(cmd, serial):
    show_version()

async def get_startup_info(cmd, serial):
    startup = StartupService()
    startup.get_startup_info()

async def set_startup_service(cmd, serial, service):
    startup = StartupService()
    startup.toggle_startup_service(service)

async def rtc_read(cmd, serial):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    ts = rtc.now()
    serial.write((RTCService.format(ts) + "\r\n").encode())

async def rtc_set(cmd, serial, yyyy, mm, dd, HH, MM, SS):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    y, mo, d, h, mi, s = map(int, (yyyy, mm, dd, HH, MM, SS))
    rtc.set_ymd_hms(y, mo, d, h, mi, s)
    serial.write(b"[RTC] Fecha y hora actualizada\r\n")

async def wifi_read(cmd, serial):
    wifi = get_wifi()
    wifi.get_wifi_info()

async def wifi_write(cmd, serial, input_string: str):
    fn = cmd.sub_code
    wifi = get_wifi()

    if fn == "s":
        wifi.set_ssid(str(input_string))
        serial.write(b"[WIFI] SSID actualizado\r\n")
    elif fn == "p":
        wifi.set_password(str(input_string))
        serial.write(b"[WIFI] Clave actualizada\r\n")
    else:
        serial.write(b"[WIFI] Comando desconocido")

async def wifi_connect(cmd, serial):
    wifi = get_wifi()

    wifi.connect()

async def wifi_disconnect(cmd, serial):
    wifi = get_wifi()

    wifi.disconnect()

COMANDOS = {
    "?": (get_help, 0),
    "e": (get_version, 0),
    "s": (get_startup_info, 0),
    "S": (set_startup_service, 1),
    "H": (rtc_set, 6),
    "h": (rtc_read, 0),
    "w": (wifi_read, 0),
    "W": {
        "c": (wifi_connect, 0),
        "d": (wifi_disconnect, 0),
        "s": (wifi_write, 1),
        "p": (wifi_write, 1),
    },
}