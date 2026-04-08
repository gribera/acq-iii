import time
from utils.hardware import get_uart
from core.memory import MemoryService

from config import (MEMORIAS,
                    WIFI_DATA_STORAGE,
                    WIFI_SSID_START_ADDRESS,
                    WIFI_SSID_LENGTH,
                    WIFI_PASS_START_ADDRESS,
                    WIFI_PASS_LENGTH)

_instance = None

class WiFiService:
    """
    Servicio para controlar el módulo ESP8266 mediante comandos AT.
    Se comunica a través de UART3 (TX3/RX3).
    """

    def __init__(self, uart_index: int = 3):
        self._transport = None

        self.ip_address = None
        self.gateway = None
        self.netmask = None


        mem = MemoryService()
        self._ssid = mem.read_string(MEMORIAS[WIFI_DATA_STORAGE],
                                     WIFI_SSID_START_ADDRESS,
                                     WIFI_SSID_LENGTH)
        self._password = mem.read_string(MEMORIAS[WIFI_DATA_STORAGE],
                                         WIFI_PASS_START_ADDRESS,
                                         WIFI_PASS_LENGTH)
        mem.close()

        self._uart = get_uart(uart_index, baudrate=115200)

    def set_transport(self, transport):
        """
        Define el 'terminal' actual (USB, WiFi, etc.).
        Debe tener un método .write(...)
        """
        self._transport = transport

    def read(self, nbytes: int = 1):
        return self._uart.read(nbytes)

    def write(self, data):
        if isinstance(data, str):
            data_bytes = data.encode("utf-8")
        else:
            data_bytes = data

        length = len(data_bytes)
        if length == 0:
            return

        cipsend_cmd = f"AT+CIPSEND=0,{length}\r\n"

        self._uart.write(cipsend_cmd.encode("utf-8"))

        time.sleep(0.1)

        resp = self._uart.read(64) or b""

        self._uart.write(data_bytes)

        time.sleep(0.1)

    def set_ssid(self, ssid: str):
        if len(ssid) > WIFI_SSID_LENGTH:
            raise ValueError("Excede el tamaño máximo para un SSID")

        mem = MemoryService()
        mem.write_string(MEMORIAS[WIFI_DATA_STORAGE], WIFI_SSID_START_ADDRESS, ssid, True)
        mem.close()
        self._ssid = ssid
        self._out("[WIFI] SSID actualizado\r\n")

    def set_password(self, password: str):
        if len(password) > WIFI_PASS_LENGTH:
            raise ValueError("Excede el tamaño máximo para un SSID")

        mem = MemoryService()
        mem.write_string(MEMORIAS[WIFI_DATA_STORAGE], WIFI_PASS_START_ADDRESS, password, True)
        mem.close()
        self._password = password
        self._out("[WIFI] Clave actualizada\r\n")

    def connect(self):
        if self.ip_address:
            self._out(f"[WiFi] Ya se encuentra conectado a {self._ssid}.")
            return

        comandos = [
            ("ATE0", 1),
            ("AT+CWMODE=1", 1),
            ("AT+CWAUTOCONN=0", 1),
            ("AT+CWQAP", 1),
            (f'AT+CWJAP="{self._ssid}","{self._password}"', 10),
            ("AT+CIPMUX=1", 1),
            ("AT+CIPSERVER=1,80", 1),
            ("AT+CIPSTA?", 1),
        ]

        self._out(f"[WiFi] Iniciando conexión a {self._ssid}.")
        for cmd, timeout in comandos:
            self._out(".")
            self._send(cmd)
            resp = self._read_response(timeout=timeout)

            if not "OK" in resp:
                self._out(f"\n[WiFi] No se pudo conectar a {self._ssid}")
                break

            if cmd.startswith("AT+CIPSTA"):
                self._parse_connection_data(resp)
                self._out("OK\r\n") # Conexión terminada y datos de conexión guardados

    def disconnect(self) -> str:
        self._out("[WiFi]")
        if not self.ip_address:
            self._out("No hay conexión activa")
            return "ERROR"

        self._send("AT+CWQAP")
        resp = self._read_response(timeout=3)
        if "OK" in resp:
            self.ip_address = None
            self._out("Desconectado.")
        else:
            self._out("Error al intentar desconectar.")

        return resp

    def get_wifi_info(self):
        if self.ip_address:
            self._out(f"[WiFi] Conectado a {self._ssid}\r\n")
            self._out(f"[WiFi] IP: {self.ip_address}\r\n")
            self._out(f"[WiFi] Gateway: {self.gateway}\r\n")
            self._out(f"[WiFi] Netmask: {self.netmask}\r\n")
        else:
            self._out("[WiFi] No conectado\r\n")

    def _send(self, command: str):
        """Envía un comando AT al módulo."""
        self._uart.write((command + "\r\n").encode("utf-8"))

    def _read_response(self, timeout: float = 2.0) -> str:
        """Lee la respuesta del módulo hasta que se detiene o vence el timeout."""
        start = time.monotonic()
        response = b""
        while time.monotonic() - start < timeout:
            data = self._uart.read(100)
            if data:
                response += data
            else:
                for _ in range(5):
                    # liberar CPU por micro-ratitos
                    pass
        if response:
            result = response.decode("utf-8")
            return result

        return ""

    def _check_ok(self, response: str):
        """Evalúa si el comando fue aceptado."""
        return "OK" in response and "ERROR" not in response

    def _parse_connection_data(self, resp: str):
        if "+CIPSTA:ip" in resp:
            ip = resp.split('ip:"')[1].split('"')[0]
            self.ip_address = ip
        if "+CIPSTA:gateway" in resp:
            gateway = resp.split('gateway:"')[1].split('"')[0]
            self.gateway = gateway
        if "+CIPSTA:netmask" in resp:
            netmask = resp.split('netmask:"')[1].split('"')[0]
            self.netmask = netmask

    def _out(self, msg: str):
        if self._transport is not None:
            self._transport.write(msg)
        else:
            print(msg, end="")

def get_wifi(uart_index: int = 3):
    """Devuelve una instancia compartida de WiFiService."""
    global _instance
    if _instance is None:
        _instance = WiFiService(uart_index)
    return _instance
