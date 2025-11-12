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

