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

    def set_ssid(self, ssid: str):
        if len(ssid) > WIFI_SSID_LENGTH:
            raise ValueError("Excede el tamaño máximo para un SSID")

        mem = MemoryService()
        mem.write_string(MEMORIAS[WIFI_DATA_STORAGE], WIFI_SSID_START_ADDRESS, ssid, True)
        mem.close()
        self._ssid = ssid

    def set_password(self, password: str):
        if len(password) > WIFI_PASS_LENGTH:
            raise ValueError("Excede el tamaño máximo para un SSID")

        mem = MemoryService()
        mem.write_string(MEMORIAS[WIFI_DATA_STORAGE], WIFI_PASS_START_ADDRESS, password, True)
        mem.close()
        self._password = password

    def connect(self):
        if self.ip_address:
            print(f"[WiFi] Ya se encuentra conectado a {self._ssid}.")
            return

        comandos = [
            ("ATE0", 1),
            ("AT+CWMODE=1", 1),
            ("AT+CWAUTOCONN=0", 1),
            ("AT+CWQAP", 1),
            (f'AT+CWJAP="{self._ssid}","{self._password}"', 10),
            ("AT+CIPSTA?", 1),
            # ("AT+CIPMUX=1", 1),
            # ("AT+CIPSERVER=1,80", 1),
        ]

        print(f"[WiFi] Iniciando conexión a {self._ssid}.", end="")
        for cmd, timeout in comandos:
            print(".", end="")
            self._send(cmd)
            resp = self._read_response(timeout=timeout)
            if not "OK" in resp:
                print(f"\n[WiFi] No se pudo conectar a {self._ssid}")
                break

            if cmd.startswith("AT+CIPSTA"):
                self._parse_connection_data(resp)
                print("OK") # Conexión terminada y datos de conexión guardados

    def disconnect(self) -> str:
        print("[WiFi]", end=" ")
        if not self.ip_address:
            print("No hay conexión activa")
            return "ERROR"

        self._send("AT+CWQAP")
        resp = self._read_response(timeout=3)
        if "OK" in resp:
            self.ip_address = None
            print("Desconectado.")
        else:
            print("Error al intentar desconectar.")

        return resp

    def get_wifi_info(self):
        if self.ip_address:
            print(f"[WiFi] Conectado a {self._ssid}")
            print(f"[WiFi] IP: {self.ip_address}")
            print(f"[WiFi] Gateway: {self.gateway}")
            print(f"[WiFi] Netmask: {self.netmask}")
        else:
            print("[WiFi] No conectado")

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
                time.sleep(0.05)
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

def get_wifi(uart_index: int = 3):
    """Devuelve una instancia compartida de WiFiService."""
    global _instance
    if _instance is None:
        _instance = WiFiService(uart_index)
    return _instance
