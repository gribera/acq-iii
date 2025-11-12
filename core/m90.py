import asyncio
import digitalio
import board

from utils.hardware import get_spi

class M90Service:
    def __init__(self, serial, spi=None, cs_pin=board.D53, led_pin=board.LED):
        self.serial = serial
        self.spi = spi or get_spi()
        self.cs = digitalio.DigitalInOut(cs_pin)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.led = digitalio.DigitalInOut(led_pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self._logging = False

    async def start_logging(self, filename="/VoltajePrueba.txt", interval=1.0):
        self.logging = True
        with open(filename, "a") as fp:
            while self.logging:
                UrmsC = await self.read_voltage()
                self.serial.write(f"UrmsC = {UrmsC:.2f} V\n\r".encode())
                fp.write(f"{UrmsC:.2f}\n")
                fp.flush()
                await asyncio.sleep(interval)

    async def stop_logging(self):
        self.serial.write(b"Logging M90 detenido.\n\r")
        self.logging = False

    async def read_voltage(self):
        spi_out_buffer = bytearray([0x80, 0xDB])
        spi_in_buffer = bytearray(2)
        self.cs.value = False
        self.spi.write(spi_out_buffer)
        self.spi.readinto(spi_in_buffer)
        self.cs.value = True
        UrmsC = int.from_bytes(spi_in_buffer, "big")

        spi_out_buffer = bytearray([0x80, 0xEB])
        spi_in_buffer = bytearray(2)
        self.cs.value = False
        self.spi.write(spi_out_buffer)
        self.spi.readinto(spi_in_buffer)
        self.cs.value = True
        UrmsCLSB = int.from_bytes(spi_in_buffer, "big")

        voltage = 0.01 * UrmsC + UrmsCLSB / 65536
        return voltage