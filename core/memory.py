import time
import digitalio

from utils.hardware import get_i2c
from config import MEMORIAS
from pins import MEM_WP

class MemoryService:
    def __init__(self, write_protect_pin=MEM_WP):
        self.i2c = get_i2c()
        self.wp = digitalio.DigitalInOut(write_protect_pin)
        self.wp.direction = digitalio.Direction.OUTPUT
        self._enable_write_protect()

    def write_string(self, memoria: int, mem_addr: int, text: str, null_terminated: bool = False):
        """
        Escribe un string en la memoria indicada.

        Args:
            memoria (str): Dirección del dispositivo ("E1", "E2" o "RTC").
            mem_addr (int): Dirección de inicio donde se escribirá el string.
            text (str): String a escribir.
            null_terminated (bool): Agrega caracter de fin de string

        Returns:
            None
        """
        self.address = memoria
        data = text.encode('ascii')
        if null_terminated:
            data = data + b'\x00'

        if memoria == MEMORIAS["RTC"]:
            self._write_bytes_rtc(mem_addr, data)
        else:
            self._write_bytes(mem_addr, data)


    def read_string(self, memoria: int, mem_addr: int, length: int) -> str:
        """
        Lee un string desde la memoria indicada.

        Args:
            memoria (str): Dirección del dispositivo ("E1", "E2" o "RTC").
            mem_addr (int): Dirección de inicio desde donde se comenzará a leer.
            length (int): Cantidad de bytes a leer.

        Returns:
            str: String leído desde la memoria.
        """
        self.address = memoria
        if memoria == MEMORIAS["RTC"]:
            data =  self._read_bytes_rtc(mem_addr, length)
        else:
            data = self._read_bytes(mem_addr, length)

        text_bytes = bytearray()
        for b in data:
            if b == 0x00:
                break
            if 32 <= b < 127:
                text_bytes.append(b)

        return text_bytes.decode('ascii')

    def _disable_write_protect(self):
        self.wp.value = False

    def _enable_write_protect(self):
        self.wp.value = True

    def _write_bytes(self, mem_addr: int, data: bytes):
        addr_high = (mem_addr >> 8) & 0xFF
        addr_low = mem_addr & 0xFF
        payload = bytes([addr_high, addr_low]) + data
        self._disable_write_protect()

        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.address, payload)
        finally:
            self.i2c.unlock()

        self._enable_write_protect()
        time.sleep(0.1)

    def _read_bytes(self, mem_addr: int, length: int) -> bytes:
        addr_high = (mem_addr >> 8) & 0xFF
        addr_low = mem_addr & 0xFF
        out_buf = bytes([addr_high, addr_low])
        in_buf = bytearray(length)

        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto_then_readfrom(self.address, out_buf, in_buf)
        finally:
            self.i2c.unlock()

        return bytes(in_buf)

    def close(self):
        if self.wp:
            self.wp.deinit()
            self.wp = None

    def __del__(self):
        self.close()

    def _write_bytes_rtc(self, start_addr: int, data: bytes):
        if not (0x08 <= start_addr <= 0x3F):
            raise ValueError("Dirección fuera de rango (0x08–0x3F)")
        if start_addr + len(data) > 0x40:
            raise ValueError("Excede el tamaño de la RAM (56 bytes)")

        while not self.i2c.try_lock():
            pass
        try:
            # a diferencia de las otras e2 se guarda byte a byte
            for i, b in enumerate(data):
                self.i2c.writeto(self.address, bytes([start_addr + i, b]))
                time.sleep(0.005)
        finally:
            self.i2c.unlock()

    def _read_bytes_rtc(self, start_addr: int, length: int) -> bytes:
        if not (0x08 <= start_addr <= 0x3F):
            raise ValueError("Dirección fuera de rango (0x08–0x3F)")
        if start_addr + length > 0x40:
            raise ValueError("Excede el tamaño de la RAM (56 bytes)")

        out_buf = bytes([start_addr])
        in_buf = bytearray(length)
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto_then_readfrom(self.address, out_buf, in_buf)
        finally:
            self.i2c.unlock()
        return bytes(in_buf)
