import board
import busio

"""
Estás funciones sirven para compartir los buses y no instanciarlos cada vez que se llaman
"""

_i2c = None
_spi = None
_uart = None

def get_i2c():
    """Devuelve una única instancia compartida de I2C"""
    global _i2c
    if _i2c is None:
        _i2c = busio.I2C(board.SCL, board.SDA)
    return _i2c

def get_spi():
    """Devuelve una única instancia compartida de SPI"""
    global _spi
    if _spi is None:
        _spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        while not _spi.try_lock():
            pass
        _spi.configure(baudrate=500000, phase=0, polarity=0)
        _spi.unlock()
    return _spi

async def run_scan_i2c(cmd, serial):
    """Escanea el bus I2C y reporta los dispositivos detectados."""
    i2c = get_i2c()

    # Esperar lock del bus
    while not i2c.try_lock():
        pass

    try:
        devices = i2c.scan()
    finally:
        i2c.unlock()

    if not devices:
        serial.write(b"No se detectaron dispositivos I2C.\r\n")
        return

    serial.write(b"Dispositivos I2C encontrados:\r\n")
    for addr in devices:
        tipo = ""
        if addr == 0x68:
            tipo = " (RTC DS1307)"
        elif 0x50 <= addr <= 0x57:
            tipo = " (EEPROM 24Cxx)"
        else:
            tipo = " (Desconocido)"
        serial.write(f" - {hex(addr)}{tipo}\r\n".encode())
# def get_uart():
#     global _uart
#     if _uart is None:
#         _uart = busio.UART(board.TX, board.RX, baudrate=115200)
#     return _uart
