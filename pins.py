import board

# I2C (EEPROM, RTC)
I2C_SCL = board.SCL
I2C_SDA = board.SDA

# SPI (M90E36A, Ethernet)
SPI_SCK  = board.SCK
SPI_MOSI = board.MOSI
SPI_MISO = board.MISO

# SPI SD card
SD_SCK  = board.SD_SCK
SD_MOSI = board.SD_MOSI
SD_MISO = board.SD_MISO

# consola
UART1_TX = board.TX
UART1_RX = board.RX

# RS485
UART2_TX = board.TX2
UART2_RX = board.RX2

# WiFi (ESP8266)
UART3_TX = board.TX3
UART3_RX = board.RX3

# Leds
LED     = board.LED
LED_TST = board.D43

# M90E36A
M90_CS = board.D53

# EEPROM
MEM_WP = board.D34          # Write protect

# Entrada analógica
AI = [
    board.A2,
    board.A3,
    board.A4,
    board.A5,
    board.A6,
    board.A7,
    board.A8,
    board.A9,
]

# Entrada analógica (InAmps)
AI_INAMP = [
    board.A12,
    board.A13,
    board.A14,
    board.A15,
]

# escritura/reset de los InAmps
INAMP_WR = [
    board.D35,  # Canal 0
    board.D36,  # Canal 1
    board.D37,  # Canal 2
    board.D38,  # Canal 3
]

# Salida analógica
AO = [
    board.A0,
    board.A1,
]

# Entrada digital
DI = [
    board.D22,
    board.D23,
    board.D26,
    board.D27,
    board.D28,
    board.D29,
    board.D30,
    board.D31,
]

# Salida digital (RELES)
DO_RELAY = [
    board.D6,
    board.D7,
    board.D8,
    board.D9,
]

# Salida digital (PWM)
PWM_OUT = [
    board.D2,
    board.D3,
    board.D4,
    board.D5,
]
