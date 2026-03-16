import asyncio
import analogio
import digitalio

from pins import AI, DI
from core.memory import MemoryService
from core.rtc import RTCService
from config import (MEMORIAS,
                    RTC_ADDR_MODO,
                    RTC_ADDR_CANT_ANALOG1,
                    RTC_ADDR_PUMEM,
                    RTC_ADDR_CODIGO,
                    RTC_ADDR_REG_FLAG,
                    RTC_ADDR_TIEMPO_REG,
                    MEM_RECORDING_DEVICE,
                    MEM_FIN_REG,
                    CODIGO_IDLE,
                    CODIGO_REGISTRO,
                    CODIGO_DESCARGA)

_instance = None


class ACQService:
    def __init__(self):
        mem = MemoryService()
        self._modo         = mem.read_byte(MEMORIAS["RTC"], RTC_ADDR_MODO)
        self._cant_analog1 = mem.read_byte(MEMORIAS["RTC"], RTC_ADDR_CANT_ANALOG1)
        self._reg_flag     = mem.read_byte(MEMORIAS["RTC"], RTC_ADDR_REG_FLAG)
        self._pumem        = self._load_pumem(mem)
        self._tiempo_reg   = self._load_tiempo_reg(mem)
        mem.close()

        if self._modo < 1 or self._modo > 5:
            self._modo = 1
        if self._cant_analog1 < 1 or self._cant_analog1 > 8:
            self._cant_analog1 = 8
        if self._reg_flag > 1:
            self._reg_flag = 0

        self._mem_full = self._pumem >= MEM_FIN_REG
        self._task = None

        self._ai = [analogio.AnalogIn(pin) for pin in AI] # Prepara los canales como entradas analógicas

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

    @property
    def reg_flag(self):
        return self._reg_flag

    @property
    def pumem(self):
        return self._pumem

    # ── Configuración ─────────────────────────────────────────────────────────

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

    # ── Modo 1: lectura en tiempo real ────────────────────────────────────────

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

    def transmit_analog(self, transport, interval):
        """
        Envía la lectura de los canales activos (Modo 1).
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

    def start_recording(self, tiempo_reg: int, transport):
        """
        Inicia el registro periódico en EEPROM (Modo 2).

        Args:
            tiempo_reg: intervalo de registro en segundos (1-3600).
        """
        if tiempo_reg < 1 or tiempo_reg > 3600:
            raise ValueError("Intervalo debe ser entre 1 y 3600 segundos")
        if self._reg_flag:
            raise ValueError("Ya hay un registro en curso")
        if self._mem_full:
            raise ValueError("Memoria llena, descargue los datos primero (ESC D)")

        self._tiempo_reg = tiempo_reg
        self._reg_flag = 1

        mem = MemoryService()
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_CODIGO, CODIGO_REGISTRO)
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_REG_FLAG, 1)
        mem.write_bytes(MEMORIAS["RTC"], RTC_ADDR_TIEMPO_REG,
                        bytes([tiempo_reg & 0xFF, (tiempo_reg >> 8) & 0xFF]))
        self._write_header(mem)
        mem.close()

        self._task = asyncio.create_task(self._recording_loop(transport))

    def stop_recording(self):
        """Detiene el registro en curso."""
        self._reg_flag = 0
        if self._task is not None:
            self._task.cancel()
            self._task = None
        mem = MemoryService()
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_REG_FLAG, 0)
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_CODIGO, CODIGO_IDLE)
        mem.close()

    def download(self, transport):
        """
        Descarga todos los datos grabados en EEPROM.
        """
        self.stop_recording()

        p = self._pumem
        # Envía 4 bytes con el valor de _pumem (cantidad de bytes a descargar)
        transport.write(bytes([
            (p >> 24) & 0xFF,
            (p >> 16) & 0xFF,
            (p >>  8) & 0xFF,
             p        & 0xFF,
        ]))

        mem = MemoryService()
        addr = 0
        chunk = 64
        # Recorre la EEPROM desde addr = 0 a _pumem y envía en fragmentos de 64 bytes
        while addr < p:
            size = min(chunk, p - addr)
            data = mem.read_bytes(MEMORIAS[MEM_RECORDING_DEVICE], addr, size)
            transport.write(data)
            addr += size

        # Resetear puntero y marcar descarga
        self._pumem = 0
        self._mem_full = False
        self._save_pumem(mem)
        mem.write_byte(MEMORIAS["RTC"], RTC_ADDR_CODIGO, CODIGO_DESCARGA)
        mem.close()

    async def _recording_loop(self, transport):
        while self._reg_flag and not self._mem_full:
            await asyncio.sleep(self._tiempo_reg)
            if not self._reg_flag:
                break
            mem = MemoryService()
            self._write_sample(mem)
            mem.close()
            transport.write(b".")

        if self._mem_full:
            self.stop_recording()
            transport.write(b"\r\n[ACQ] Memoria llena\r\n")

    def _write_header(self, mem):
        """
        Escribe el header de 27 bytes al inicio del registro.

        [0xFF][0xFF]
        [ss][mm][hh][dow][dd][MM][yy][0x00][0x00][0x00]  ← 10 bytes tiempo (BCD)
        [0x32][0x30]                                       ← "20" prefijo año
        [yy_decenas_ASCII][yy_unidades_ASCII]             ← año últimos 2 dígitos
        [t_reg_str 4 bytes ASCII]                         ← e.g. "0060"
        [modo][cant_analog1][cant_analog2][0x08][0x01]    ← 5 bytes config
        [0xFF][0xFF]                                       ← fin
        """
        rtc = RTCService()
        now = rtc.now()

        def bcd(n):
            return ((n // 10) << 4) | (n % 10)

        year2 = now.tm_year % 100 # Devuelve el resto de año/100 (ej. 2025 devuelve 25)
        t_str = "{:04d}".format(self._tiempo_reg).encode() # F

        header = bytearray()
        header += b'\xff\xff'
        header += bytes([
            bcd(now.tm_sec), bcd(now.tm_min), bcd(now.tm_hour),
            now.tm_wday, bcd(now.tm_mday), bcd(now.tm_mon), bcd(year2),
            0x00, 0x00, 0x00,
        ])
        header += b'\x32\x30'
        header += bytes([0x30 + (year2 // 10), 0x30 + (year2 % 10)])
        header += t_str
        header += bytes([self._modo, self._cant_analog1, 0, 0x08, CODIGO_REGISTRO])
        header += b'\xff\xff'

        self._eeprom_write(mem, bytes(header))

    def _write_sample(self, mem):
        """
        Graba una muestra: 1 byte digital + N×2 bytes analógicos (little-endian).
        Formato idéntico al .ino (Registro_Temp_E2).
        """
        buf = bytearray([self.read_digital()])
        for v in self.read_analog():
            buf.append(v & 0xFF)         # LSB
            buf.append((v >> 8) & 0xFF)  # MSB
        self._eeprom_write(mem, bytes(buf))

    def _eeprom_write(self, mem, data: bytes):
        """Escribe bytes en EEPROM actualizando pumem. Detiene si memoria llena."""
        if self._mem_full:
            return
        device = MEMORIAS[MEM_RECORDING_DEVICE]
        mem.write_bytes(device, self._pumem, data)
        self._pumem += len(data)
        if self._pumem >= MEM_FIN_REG:
            self._mem_full = True
        self._save_pumem(mem)

    def _load_pumem(self, mem) -> int:
        b = mem.read_bytes(MEMORIAS["RTC"], RTC_ADDR_PUMEM, 4)
        p = b[0] | (b[1] << 8) | (b[2] << 16) | (b[3] << 24)
        return p if p <= MEM_FIN_REG else 0

    def _save_pumem(self, mem):
        p = self._pumem
        mem.write_bytes(MEMORIAS["RTC"], RTC_ADDR_PUMEM,
                        bytes([p & 0xFF, (p >> 8) & 0xFF,
                               (p >> 16) & 0xFF, (p >> 24) & 0xFF]))

    def _load_tiempo_reg(self, mem) -> int:
        b = mem.read_bytes(MEMORIAS["RTC"], RTC_ADDR_TIEMPO_REG, 2)
        t = b[0] | (b[1] << 8)
        return t if 1 <= t <= 3600 else 1

    def close(self):
        self.stop_recording()
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
