import board
import busio
import digitalio
import analogio
import time
import adafruit_ds1307
import adafruit_wiznet5k.adafruit_wiznet5k as wiznet5k
import adafruit_wiznet5k.adafruit_wiznet5k_socketpool as socketpool
# import os
# import sdcardio
# import storage

time.sleep(2.0)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

led_tst = digitalio.DigitalInOut(board.D43)
led_tst.direction = digitalio.Direction.OUTPUT
led_tst.value = False

pwm_1 = digitalio.DigitalInOut(board.D2)
pwm_1.direction = digitalio.Direction.OUTPUT
pwm_1.value = False

pwm_2 = digitalio.DigitalInOut(board.D3)
pwm_2.direction = digitalio.Direction.OUTPUT
pwm_2.value = False

pwm_3 = digitalio.DigitalInOut(board.D4)
pwm_3.direction = digitalio.Direction.OUTPUT
pwm_3.value = False

pwm_4 = digitalio.DigitalInOut(board.D5)
pwm_4.direction = digitalio.Direction.OUTPUT
pwm_4.value = False

rele_1 = digitalio.DigitalInOut(board.D6)
rele_1.direction = digitalio.Direction.OUTPUT
rele_1.value = False

rele_2 = digitalio.DigitalInOut(board.D7)
rele_2.direction = digitalio.Direction.OUTPUT
rele_2.value = False

rele_3 = digitalio.DigitalInOut(board.D8)
rele_3.direction = digitalio.Direction.OUTPUT
rele_3.value = False

rele_4 = digitalio.DigitalInOut(board.D9)
rele_4.direction = digitalio.Direction.OUTPUT
rele_4.value = False

dig_in_0 = digitalio.DigitalInOut(board.D22)
dig_in_0.direction = digitalio.Direction.INPUT

dig_in_1 = digitalio.DigitalInOut(board.D23)
dig_in_1.direction = digitalio.Direction.INPUT

dig_in_2 = digitalio.DigitalInOut(board.D26)
dig_in_2.direction = digitalio.Direction.INPUT

dig_in_3 = digitalio.DigitalInOut(board.D27)
dig_in_3.direction = digitalio.Direction.INPUT

dig_in_4 = digitalio.DigitalInOut(board.D28)
dig_in_4.direction = digitalio.Direction.INPUT

dig_in_5 = digitalio.DigitalInOut(board.D29)
dig_in_5.direction = digitalio.Direction.INPUT

dig_in_6 = digitalio.DigitalInOut(board.D30)
dig_in_6.direction = digitalio.Direction.INPUT

dig_in_7 = digitalio.DigitalInOut(board.D31)
dig_in_7.direction = digitalio.Direction.INPUT

switch = digitalio.DigitalInOut(board.D12)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

switch_sd = digitalio.DigitalInOut(board.SD_CARD_DETECT)
switch_sd.direction = digitalio.Direction.INPUT
switch_sd.pull = digitalio.Pull.UP

an_0 = analogio.AnalogIn(board.A2)
an_1 = analogio.AnalogIn(board.A3)
an_2 = analogio.AnalogIn(board.A4)
an_3 = analogio.AnalogIn(board.A5)
an_4 = analogio.AnalogIn(board.A6)
an_5 = analogio.AnalogIn(board.A7)
an_6 = analogio.AnalogIn(board.A8)
an_7 = analogio.AnalogIn(board.A9)

g_0 = digitalio.DigitalInOut(board.D39)
g_0.direction = digitalio.Direction.OUTPUT
g_0.value = False
g_1 = digitalio.DigitalInOut(board.D40)
g_1.direction = digitalio.Direction.OUTPUT
g_1.value = False
wra_1 = digitalio.DigitalInOut(board.D35)
wra_1.direction = digitalio.Direction.OUTPUT
wra_1.value = True
time.sleep(0.1)
wra_1.value = False
time.sleep(0.01)
wra_1.value = True
wra_2 = digitalio.DigitalInOut(board.D36)
wra_2.direction = digitalio.Direction.OUTPUT
wra_2.value = True
time.sleep(0.1)
wra_2.value = False
time.sleep(0.01)
wra_2.value = True
wra_3 = digitalio.DigitalInOut(board.D37)
wra_3.direction = digitalio.Direction.OUTPUT
wra_3.value = True
time.sleep(0.1)
wra_3.value = False
time.sleep(0.01)
wra_3.value = True
wra_4 = digitalio.DigitalInOut(board.D38)
wra_4.direction = digitalio.Direction.OUTPUT
wra_4.value = True
time.sleep(0.1)
wra_4.value = False
time.sleep(0.01)
wra_4.value = True

ai_0 = analogio.AnalogIn(board.A12)
ai_1 = analogio.AnalogIn(board.A13)
ai_2 = analogio.AnalogIn(board.A14)
ai_3 = analogio.AnalogIn(board.A15)

ao_0 = analogio.AnalogOut(board.A0)
ao_1 = analogio.AnalogOut(board.A1)
ao_0.value = 32768
ao_1.value = 49152
# print(an_0.reference_voltage)
# 3.3V para esta placa

cs_M90 = digitalio.DigitalInOut(board.D53)
cs_M90.direction = digitalio.Direction.OUTPUT
cs_M90.value = True

wp_e2 = digitalio.DigitalInOut(board.D34)
wp_e2.direction = digitalio.Direction.OUTPUT
wp_e2.value = True

spi_SD = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)
cs = board.SD_CS

STB_Can = digitalio.DigitalInOut(board.D42)
STB_Can.direction = digitalio.Direction.OUTPUT
STB_Can.value = False

cs_Eth = digitalio.DigitalInOut(board.D33)
cs_Eth.direction = digitalio.Direction.OUTPUT
cs_Eth.value = True
ETHERNET_RST = board.A10   # Pin digital para Reset del W5500
reset = digitalio.DigitalInOut(ETHERNET_RST)

AB_RS485 = 19200
uart2 = busio.UART(board.TX2, board.RX2, baudrate=AB_RS485)

# Pin digital para manejo de la comunicación RS232
# False = escucha el bus - True = escribe el bus
RS485_DIR = digitalio.DigitalInOut(board.D41)
RS485_DIR.direction = digitalio.Direction.OUTPUT
RS485_DIR.value = False  # Modo normal

AB_WiFi = 115200
uart3 = busio.UART(board.TX3, board.RX3, baudrate=AB_WiFi)

def enviar_RS485(caracteres):
    """Envía caracteres por R485."""
    print(f"Enviando: {caracteres}")
    RS485_DIR.value = True
    uart2.write(caracteres.encode('utf-8') + b'\r\n')
    RS485_DIR.value = False

def leer_RS485():
    respuesta = b''
    while True:
        data = uart2.read(1)
        if data:
            respuesta += data
        else:
            break
    if respuesta:
        data_string = ''.join([chr(b) for b in respuesta])
        print(data_string)

def enviar_comando_at(comando):
    """Envía un comando AT al módulo serial."""
    print(f"Enviando: {comando}")
    uart3.write(comando.encode('utf-8') + b'\r\n')

def leer_respuesta_at():
    respuesta = b''
    while True:
        data = uart3.read(100)
        if data:
            respuesta += data
        else:
            break
    if respuesta:
        data_string = ''.join([chr(b) for b in respuesta])
        print(data_string)
    return data_string

# inicialización de la placa WiFi ESP8266
def ini_WiFi():
    print()
    enviar_comando_at("ATE0")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CWAUTOCONN=0")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CWQAP")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CWJAP=\"FibertelWifi2.4GHz\",\"0043243475G\"")
    time.sleep(20.0)
    respuesta = leer_respuesta_at()
    if "FAIL" not in respuesta:
        if "ERROR" not in respuesta:
            print("Comando recibido y ejecutado")
        else:
            print("Comando no procesado o sin respuesta")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CIPSTA?")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CIPMUX=1")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

    print()
    enviar_comando_at("AT+CIPSERVER=1,80")
    time.sleep(1.0)
    respuesta = leer_respuesta_at()
    if "OK" in respuesta:
        print("Comando recibido y ejecutado")
    else:
        print("Comando no procesado o sin respuesta")

# Realizar el ping
def ejecutar_ping():
    # spi_bus = busio.SPI(board.SCK, board.MOSI, board.MISO)
    with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi:
        print("Inicializando Ethernet...")
        eth = wiznet5k.WIZNET5K(spi, cs_Eth, reset)

        print("Intentando obtener dirección IP...")
        # Espera a que el W5500 obtenga una dirección IP (si es DHCP)
        while not eth.link_status:
            print("Esperando conexión de red...")
            time.sleep(1)

        print("--- Conectado a la red ---")
        print(f"Dirección IP: {eth.pretty_ip(eth.ip_address)}")
        # print(f"Gateway: {eth.pretty_ip(eth.gateway)}")
        # print(f"Máscara de Subred: {eth.pretty_ip(eth.subnet_mask)}")
        # print(f"DNS Server: {eth.pretty_ip(eth.dns_address)}")
        print(f"MAC Address: {eth.pretty_mac(eth.mac_address)}")
        print("--------------------------")

        # Crear socket pool con la interfaz de red
        pool = socketpool.SocketPool(eth)
        # timeout = 10

        try:
            remote_ip = "192.168.0.1"
            sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
            sock.settimeout(10)
            print("sock")
            start_time = time.monotonic()
            print("start_time")
            sock.sendto(b"\x08\x00\x00\x00", (remote_ip, 1))
            print("send")
            data, addr = sock.recvfrom(1024)
            print(addr)
            end_time = time.monotonic()
            print("end_time")
            elapsed_time = (end_time - start_time) * 1000  # Tiempo en ms
            return elapsed_time
        except pool.timeout:
            return None
        finally:
            sock.close()

def set_ETH():
    # spi_bus = busio.SPI(board.SCK, board.MOSI, board.MISO)
    with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi:
        print("Inicializando Ethernet...")
        eth = wiznet5k.WIZNET5K(spi, cs_Eth, reset)

        print("Intentando obtener dirección IP...")
        # Espera a que el W5500 obtenga una dirección IP (si es DHCP)
        while not eth.link_status:
            print("Esperando conexión de red...")
            time.sleep(1)

        print("--- Conectado a la red ---")
        print(f"Dirección IP: {eth.pretty_ip(eth.ip_address)}")
        # print(f"Gateway: {eth.pretty_ip(eth.gateway)}")
        # print(f"Máscara de Subred: {eth.pretty_ip(eth.subnet_mask)}")
        # print(f"DNS Server: {eth.pretty_ip(eth.dns_address)}")
        print(f"MAC Address: {eth.pretty_mac(eth.mac_address)}")
        print("--------------------------")

def prueba_analogica():
    factor = 9.9 / 65536
    valor_in = an_0.value * factor
    print("an_0 = ", valor_in)
    valor_in = an_1.value * factor
    print("an_1 = ", valor_in)
    valor_in = an_2.value * factor
    print("an_2 = ", valor_in)
    valor_in = an_3.value * factor
    print("an_3 = ", valor_in)
    valor_in = an_4.value * factor
    print("an_4 = ", valor_in)
    valor_in = an_5.value * factor
    print("an_5 = ", valor_in)
    valor_in = an_6.value * factor
    print("an_6 = ", valor_in)
    valor_in = an_7.value * factor
    print("an_7 = ", valor_in)

    factor = 3.3 / 65536
    valor_in = ai_0.value * factor
    print("ai_0 = ", valor_in)
    valor_in = ai_1.value * factor
    print("ai_1 = ", valor_in)
    valor_in = ai_2.value * factor
    print("ai_2 = ", valor_in)
    valor_in = ai_3.value * factor
    print("ai_3 = ", valor_in)

def prueba_digital():
    if dig_in_0.value:
        rele_1.value = False
    else:
        rele_1.value = True

    if dig_in_1.value:
        rele_2.value = False
    else:
        rele_2.value = True

    if dig_in_2.value:
        rele_3.value = False
    else:
        rele_3.value = True

    if dig_in_3.value:
        rele_4.value = False
    else:
        rele_4.value = True

    if dig_in_4.value:
        pwm_1.value = False
    else:
        pwm_1.value = True

    if dig_in_5.value:
        pwm_2.value = False
    else:
        pwm_2.value = True

    if dig_in_6.value:
        pwm_3.value = False
    else:
        pwm_3.value = True

    if dig_in_7.value:
        pwm_4.value = False
    else:
        pwm_4.value = True

def prueba_M90():
    with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi:
        spi.try_lock()
        # spi.configure(baudrate=500000, phase=0, polarity=0)

        spi_out_buffer = bytearray([0x80, 0xDB])
        spi_in_buffer = bytearray([0x00, 0x00])
        cs_M90.value = False
        spi.write(spi_out_buffer)
        spi.readinto(spi_in_buffer)
        cs_M90.value = True
        UrmsC = int.from_bytes(spi_in_buffer, "big")

        spi_out_buffer = bytearray([0x80, 0xEB])
        spi_in_buffer = bytearray([0x00, 0x00])
        cs_M90.value = False
        spi.write(spi_out_buffer)
        spi.readinto(spi_in_buffer)
        cs_M90.value = True
        UrmsCLSB = int.from_bytes(spi_in_buffer, "big")

        UrmsC = 0.01 * UrmsC + UrmsCLSB / 65536
        print("UrmsC(V3) = ", UrmsC, "V")

def dispositivos_en_I2c():
    with busio.I2C(board.SCL, board.SDA) as i2c:
        while not i2c.try_lock():
            pass
        devices = i2c.scan()
        i2c.unlock()
        print("Disp. I2C:", [hex(device_address) for device_address in devices])

def prueba_e2():
    wp_e2.value = False
    with busio.I2C(board.SCL, board.SDA) as i2c:
        while not i2c.try_lock():
            pass
        # Para escritura
        # FORMATO: (DirE2_I2c, bytes([DirH, DirL, Dato1,...., Dato7]))
        # Dato: "E2 OK 1" y "E2 OK 2"
        i2c.writeto(0x50, bytes([0x00, 0x00, 0x45, 0x32, 0x20, 0x4f, 0x4B, 0x20, 0x31]))
        i2c.writeto(0x54, bytes([0x00, 0x00, 0x45, 0x32, 0x20, 0x4f, 0x4B, 0x20, 0x32]))
        wp_e2.value = True

        time.sleep(0.1)

        # Para lectura
        # FORMATO: bytearray([DirH, DirL])
        i2c_out_buffer1 = bytearray([0x00, 0x00])
        i2c_out_buffer2 = bytearray([0x00, 0x00])
        # FORMATO: bytearray(Cantidad de datos a leer)
        i2c_in_buffer1 = bytearray(7)
        i2c_in_buffer2 = bytearray(7)
        i2c.writeto_then_readfrom(0x50, i2c_out_buffer1, i2c_in_buffer1)
        i2c.writeto_then_readfrom(0x54, i2c_out_buffer2, i2c_in_buffer2)
        i2c.unlock()
        print(i2c_in_buffer1)
        print(i2c_in_buffer2)

def ensure_clock_running():
    with busio.I2C(board.SCL, board.SDA) as i2c:
        while not i2c.try_lock():
            pass
        i2c.writeto(0x68, bytes([0x00, 0x00]))
        i2c.unlock()

def set_rtc():
    with busio.I2C(board.SCL, board.SDA) as i2c:
        rtc = adafruit_ds1307.DS1307(i2c)
        # FORMATO DÍA Y HORA: (AÑO, MES, DÍA, HORA, MIN SEG, DÍA_SEMANA, -1, -1)
        t = time.struct_time((2025, 6, 23, 18, 27, 0, 2, -1, -1))
        rtc.datetime = t

def prueba_rtc():
    with busio.I2C(board.SCL, board.SDA) as i2c:
        rtc = adafruit_ds1307.DS1307(i2c)
        now = rtc.datetime
        print("{:02d}/{:02d}".format(now.tm_mday, now.tm_mon), end='')
        print("/{:04d} ".format(now.tm_year), end='')
        print("{:02d}:{:02d}:{:02d}".format(now.tm_hour, now.tm_min, now.tm_sec))

def test_ACQIII():

    while True:
        # print("Hola Mundo...")
        led.value = not led.value
        led_tst.value = not led_tst.value

        # Descomentar la función quiere probar. También pueden ser todas juntas

        # Para prueba_digital() conectar 0 o 5Vcc entre las enrtradas Di0...Di7 y COM
        # y se iran activando las salidas digitales Od0...Od3 y los Reles
        # Para prueba_analogica() conectar de 0 a 10Vcc en las entradas An0...An7
        # y conectar de 0 a 3,3Vcc en las entradas Ai0... Ai3
        # Para prueba_rtc() antes hay que descomentar el set_rtc() una vez
        # Para probar RS485: poner terminadores, un equipo en envio y el otro en lectura
        # Para prueba_M90() conectar una tensión 220Vrms entre V3 y VN

        # prueba_digital()
        # prueba_analogica()
        # prueba_e2()
        # prueba_rtc()

        # enviar_RS485("Hola Mundo")
        # leer_RS485()

        # prueba_M90()

        time.sleep(1.00)

# Programa principal

# Descomentar set_rtc() una sola vez para setear el reloj
# Antes se debe poner el día y la hora en esa función
# set_rtc()

# Solo descomentar ensure_clock_running() si hay problemas con el seteo del RTC
# ensure_clock_running()

# Descomentar dispositivos_en_I2c() para saber la dirección de los esclavos hay en I2c
# dispositivos_en_I2c()

# Descomentar set_ETH() para inicializar el port Ethernet
# set_ETH()
# ejecutar_ping()

# Descomentar ini_WiFi() para inicializar la placa WiFi ESP8266
# ini_WiFi()

test_ACQIII()
