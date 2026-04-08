# Datos versión
EQUIPO = "ACQ-III - M90E36A"
VERSION = "0.1.0"
FECHA = "18-03-2026"

# Modos de trabajo
MODO_ACQ1_ONLINE   = 1
MODO_ACQ1_REGISTRO = 2
MODO_ACQ2_ONLINE   = 3
MODO_ACQ2_REGISTRO = 4
MODO_AUI           = 5


# Rtc_m_st  08    startup byte
#    +01    09    pumem (LL) --> Puntero de memoria E2 (I2c)
#    +02    0A    pumem
#    +03    0B    pumem
#    +04    0C    pumem (HH)
#    +05    0D    cantCan_analog1 --> Cantidad canales anal�gicos
#    +06    0E    cantCan_analog2 --> Cantidad canales anal�gicos tipo inAmp
#    +07    0F    C�digo de inicio (Ver cuadro a continuaci�n)
#    +08    10    reg_flag --> Flag de registro
#    +09    11    tiempo_reg (L) --> Tiempo de registro
#    +10    12    tiempo_reg (H)
#    +11    13    modo
RTC_ADDR_PUMEM        = 0x09
RTC_ADDR_CANT_ANALOG1 = 0x0D
RTC_ADDR_CANT_ANALOG2 = 0x0E
RTC_ADDR_CODIGO       = 0x0F   # código de estado de la última operación
RTC_ADDR_REG_FLAG     = 0x10   # flag de registro activo (0=inactivo, 1=activo)
RTC_ADDR_TIEMPO_REG   = 0x11   # 2 bytes: intervalo de registro en segundos
RTC_ADDR_MODO         = 0x13

# Área de registro en EEPROM E1 (últimos 512 bytes reservados para config)
MEM_RECORDING_DEVICE = "E1"
MEM_FIN_REG          = 0xFDFF  # 65023 — último byte disponible para registro

# Códigos de estado (RTC_ADDR_CODIGO)
CODIGO_IDLE     = 0x00
CODIGO_REGISTRO = 0x01
CODIGO_DESCARGA = 0x02

# Startup (secuencia de inicio)
STARTUP_DATA_STORAGE  = "RTC"                   # Memoria del RTC para guardar el byte de startup
STARTUP_SEQUENCE_BYTE = 0x08                    # Dirección donde se va a alojar el byte de startup
STARTUP_SERVICES = {                            # Servicios disponibles para ejecutar al inicio
  "w": ("WiFi", 0)
}

# Máquina de estados
COMANDO_INICIO   = "\x1b"                       # Comando que da inicio a la recepción de comandos
COMANDO_FIN      = "\x0d"                       # Comando que da fin a la recepción de comandos
TIMEOUT_COMANDOS = 5                            # Timeout para la recepción de comandos

# Memorias
MEMORIAS = {                                    # Lista con las memorias disponibles y su respectiva
  "E1": 0x50,                                   # dirección dentro del BUS i2c
  "E2": 0x54,
  "RTC": 0x68
}

# WiFi
WIFI_DATA_STORAGE       = "E1"
WIFI_SSID_START_ADDRESS = 0xFE02                 # 32 bytes para nombre de red
WIFI_SSID_LENGTH        = 32
WIFI_PASS_START_ADDRESS = 0xFE22                 # 32 bytes para clave (0xFE02 + 32)
WIFI_PASS_LENGTH        = 32
