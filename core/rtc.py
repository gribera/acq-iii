# core/rtc.py
import time
import board
import busio
import adafruit_ds1307  # requiere lib/adafruit_ds1307.mpy

class RTCService:

    def __init__(self, i2c: busio.I2C | None = None):
        self._own_bus = False
        if i2c is None:
            i2c = busio.I2C(board.SCL, board.SDA)
            self._own_bus = True

        # Esperar a que el bus esté listo
        while not i2c.try_lock():
            pass
        i2c.unlock()

        self._i2c = i2c
        self._rtc = adafruit_ds1307.DS1307(self._i2c)

    def now(self) -> time.struct_time:
        return self._rtc.datetime

    def set_ymd_hms(self, year: int, month: int, day: int,
                    hour: int, minute: int, second: int,
                    weekday: int = -1) -> None:
        st = time.struct_time((year, month, day, hour, minute, second, weekday, -1, -1))
        self._rtc.datetime = st

    @staticmethod
    def format(ts: time.struct_time) -> str:
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec
        )

