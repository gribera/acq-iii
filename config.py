# Máquina de estados
COMANDO_INICIO = "\x1b"                         # Comando que da inicio a la recepción de comandos
COMANDO_FIN = "\x0d"                            # Comando que da fin a la recepción de comandos
TIMEOUT_COMANDOS = 5                            # Timeout para la recepción de comandos

# EEPROM
E2 = {
  "E1": 0x50,
  "E2": 0x54,
  "RTC": 0x68
}
