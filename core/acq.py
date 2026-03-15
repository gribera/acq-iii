import analogio
import digitalio

from pins import AI, DI
from core.memory import MemoryService
from config import (MEMORIAS,
                    RTC_ADDR_MODO,
                    RTC_ADDR_CANT_ANALOG1)

_instance = None


class ACQService:
    def __init__(self):
        mem = MemoryService()
        self._modo         = mem.read_byte(MEMORIAS["RTC"], RTC_ADDR_MODO)
        self._cant_analog1 = mem.read_byte(MEMORIAS["RTC"], RTC_ADDR_CANT_ANALOG1)
        mem.close()

        if self._modo < 1 or self._modo > 5:
            self._modo = 1 # Modo 1 por defecto
        if self._cant_analog1 < 1 or self._cant_analog1 > 8:
            self._cant_analog1 = 8 # 8 Canales por defecto

        self._ai = [analogio.AnalogIn(pin) for pin in AI]

        self._di = []
        for pin in DI:
            d = digitalio.DigitalInOut(pin)
            d.direction = digitalio.Direction.INPUT
            self._di.append(d)

    @property
    def modo(self):
        return self._modo

    @property
    def cant_analog1(self):
        return self._cant_analog1

    def set_modo(self, modo: int):
        if modo < 1 or modo > 5:
            raise ValueError("Modo debe ser entre 1 y 5")
        self._modo = modo
        mem = MemoryService()
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_MODO, modo)
        mem.close()

    def set_cant_analog1(self, n: int):
        if n < 1 or n > 8:
            raise ValueError("Cantidad de canales debe ser entre 1 y 8")
        self._cant_analog1 = n
        mem = MemoryService()
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_CANT_ANALOG1, n)
        mem.close()

    def read_analog(self):
        """
        Lee los canales analógicos activos.

        Returns:
            list[int]: valores 12-bit (0-4095), uno por canal activo.
        """
        result = []
        for i in range(self._cant_analog1):
            raw = self._ai[i].value   # 16-bit (0-65535)
            result.append(raw >> 4)   # → 12-bit (0-4095)
        return result

    def read_digital(self) -> int:
        """
        Lee los 8 canales digitales de entrada.

        Returns:
            int: byte con un bit por canal (bit 0 = DI[0], ..., bit 7 = DI[7]).
        """
        byte_val = 0
        for i, pin in enumerate(self._di):
            if pin.value:
                byte_val |= (1 << i)
        return byte_val

    def transmit_analog(self, transport):
        """
        Envía la lectura de los canales analógicos activos.

        Formato: [CANAL0_HIGH][CANAL0_LOW] ... [CANAL(N-1)_HIGH][CANAL(N-1)_LOW]
        """
        values = self.read_analog()
        buf = bytearray()
        for v in values:
            buf.append((v >> 8) & 0xFF)
            buf.append(v & 0xFF)
        transport.write(bytes(buf))

    def transmit_digital(self, transport):
        """Envía 1 byte con el estado de las 8 entradas digitales."""
        transport.write(bytes([self.read_digital()]))

    def close(self):
        for pin in self._ai:
            pin.deinit()
        for pin in self._di:
            pin.deinit()


def get_acq():
    """Devuelve una instancia compartida de ACQService."""
    global _instance
    if _instance is None:
        _instance = ACQService()
    return _instance
