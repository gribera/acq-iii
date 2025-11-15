# Datos versión
EQUIPO = "ACQ-III - M90E36A"
VERSION = "0.0.1"
FECHA = "15-11-2025"

# Startup (secuencia de inicio)
STARTUP_DATA_STORAGE = "RTC"                    # Memoria del RTC para guardar el byte de startup
STARTUP_SEQUENCE_BYTE = 0x08                    # Dirección donde se va a alojar el byte de startup
STARTUP_SERVICES = {                            # Servicios disponibles para ejecutar al inicio
  "w": ("WiFi", 0)
}

# Máquina de estados
COMANDO_INICIO = "\x1b"                         # Comando que da inicio a la recepción de comandos
COMANDO_FIN = "\x0d"                            # Comando que da fin a la recepción de comandos
TIMEOUT_COMANDOS = 5                            # Timeout para la recepción de comandos

# Memorias
MEMORIAS = {                                    # Lista con las memorias disponibles y su respectiva
  "E1": 0x50,                                   # dirección dentro del BUS i2c
  "E2": 0x54,
  "RTC": 0x68
}

# WiFi
WIFI_DATA_STORAGE = "RTC"                        # Memoria del RTC para guardar datos de conexión
WIFI_SSID_START_ADDRESS = 0x09                   # Inicio de guardado del Access Point
WIFI_SSID_LENGTH = 20                            # Cantidad de bytes reservados para el AP
WIFI_PASS_START_ADDRESS = 0x1D                   # Inicio de guardado de la clave
WIFI_PASS_LENGTH = 20                            # Cantidad de bytes reservados para la clave
