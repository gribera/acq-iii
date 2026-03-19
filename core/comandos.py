import asyncio
import busio
import board

from utils.help import show_help, show_version
from core.startup import StartupService
from core.rtc import RTCService
from core.wifi import get_wifi
from core.acq import get_acq

async def get_help(cmd, transport):
    await show_help(transport)

async def get_version(cmd, transport):
    await show_version(transport)

async def get_startup_info(cmd, transport):
    startup = StartupService()
    startup.set_transport(transport)
    startup.get_startup_info()

async def set_startup_service(cmd, transport, service):
    startup = StartupService()
    startup.set_transport(transport)
    startup.toggle_startup_service(service)

async def rtc_read(cmd, transport):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    ts = rtc.now()
    transport.write((RTCService.format(ts) + "\r\n").encode())

async def rtc_set(cmd, transport, yyyy, mm, dd, HH, MM, SS):
    rtc = getattr(cmd, "rtc", None) or RTCService()
    cmd.rtc = rtc
    y, mo, d, h, mi, s = map(int, (yyyy, mm, dd, HH, MM, SS))
    rtc.set_ymd_hms(y, mo, d, h, mi, s)
    transport.write(b"[RTC] Fecha y hora actualizada\r\n")

async def wifi_read(cmd, transport):
    wifi = get_wifi()
    wifi.set_transport(transport)
    wifi.get_wifi_info()

async def wifi_write(cmd, transport, input_string: str):
    fn = cmd.sub_code
    wifi = get_wifi()
    wifi.set_transport(transport)

    if fn == "s":
        wifi.set_ssid(str(input_string))
    elif fn == "p":
        wifi.set_password(str(input_string))

async def wifi_connect(cmd, transport):
    wifi = get_wifi()
    wifi.set_transport(transport)

    wifi.connect()

async def wifi_disconnect(cmd, transport):
    wifi = get_wifi()
    wifi.set_transport(transport)

    wifi.disconnect()

async def acq_start_recording(cmd, transport, tiempo_reg):
    acq = get_acq()
    try:
        acq.start_recording(int(tiempo_reg), transport)
        transport.write(f"[ACQ] Registro iniciado cada {tiempo_reg}s\r\n".encode())
    except ValueError as e:
        transport.write(f"[ACQ] Error: {e}\r\n".encode())

async def acq_stop_recording(cmd, transport):
    acq = get_acq()
    acq.stop_recording()
    transport.write(b"[ACQ] Registro detenido\r\n")

async def acq_download(cmd, transport):
    acq = get_acq()
    acq.download(transport)

async def acq_set_modo(cmd, transport, modo):
    acq = get_acq()
    try:
        acq.set_modo(int(modo))
        transport.write(f"[ACQ] Modo {modo} configurado\r\n".encode())
    except ValueError as e:
        transport.write(f"[ACQ] Error: {e}\r\n".encode())

async def acq_set_canales(cmd, transport, n):
    acq = get_acq()
    try:
        acq.set_cant_analog1(int(n))
        transport.write(f"[ACQ] Canales analógicos activos: {n}\r\n".encode())
    except ValueError as e:
        transport.write(f"[ACQ] Error: {e}\r\n".encode())

async def acq_transmitir(cmd, transport, interval):
    acq = get_acq()
    try:
        acq.start_transmit(transport, int(interval))
    except ValueError as e:
        transport.write(f"[ACQ] Error: {e}\r\n".encode())

async def acq_stop_transmitir(cmd, transport):
    acq = get_acq()
    acq = acq.stop_transmit(transport)

async def acq_leer_digital(cmd, transport):
    acq = get_acq()
    acq.transmit_digital(transport)

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
    "E": (acq_set_modo, 1),
    "A": (acq_set_canales, 1),
    "R": {
        "s": (acq_start_recording, 1),
        "p": (acq_stop_recording, 0),
        "d": (acq_download, 0),
    },
    "L": {
        "s": (acq_transmitir, 1),
        "p": (acq_stop_transmitir, 0),
        "u": (acq_leer_digital, 0),
    }
}