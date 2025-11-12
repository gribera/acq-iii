import time
import adafruit_ds1307
from utils.hardware import get_i2c

class RTCService:
    def __init__(self):
        self._rtc = adafruit_ds1307.DS1307(get_i2c())

    def now(self):
        return self._rtc.datetime

    def set_ymd_hms(self, y, m, d, hh, mm, ss, weekday=-1):
        """
        Configura la fecha y hora actual del RTC (Real Time Clock).

        Args:
            y (int): Año (formato yyyy).
            m (int): Mes (1–12).
            d (int): Día del mes (1–31).
            hh (int): Hora en formato 24 horas (0–23).
            mm (int): Minutos (0–59).
            ss (int): Segundos (0–59).
            weekday (int, optional): Día de la semana (0=lunes … 6=domingo).
                Por defecto -1 para que el RTC lo calcule automáticamente.

        Returns:
            None
        """
        ts = time.struct_time((y, m, d, hh, mm, ss, weekday, -1, -1))
        self._set_datetime(ts)

    def _set_datetime(self, ts):
        """
        Devuelve la fecha y hora actual del RTC.

        Returns:
            time.struct_time: Objeto con la fecha y hora actual.
        """
        self._rtc.datetime = ts

    @staticmethod
    def format(ts):
        return f"{ts.tm_year:04d}-{ts.tm_mon:02d}-{ts.tm_mday:02d} {ts.tm_hour:02d}:{ts.tm_min:02d}:{ts.tm_sec:02d}"
