import time
import adafruit_ds1307
from utils.hardware import get_i2c

class RTCService:
    def __init__(self):
        self._rtc = adafruit_ds1307.DS1307(get_i2c())

    def now(self):
        return self._rtc.datetime

    def set_datetime(self, ts):
        self._rtc.datetime = ts

    def set_ymd_hms(self, y, m, d, hh, mm, ss, weekday=-1):
        ts = time.struct_time((y, m, d, hh, mm, ss, weekday, -1, -1))
        self.set_datetime(ts)

    @staticmethod
    def format(ts):
        return f"{ts.tm_year:04d}-{ts.tm_mon:02d}-{ts.tm_mday:02d} {ts.tm_hour:02d}:{ts.tm_min:02d}:{ts.tm_sec:02d}"
