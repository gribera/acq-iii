import time

CR_LF = "\n\r"

class Registro:
    def __init__(self, serial):
        self.serial = serial

    def iniciar_registro(self, num, total):
        for x in range(total):
            self.serial.write(f"{num}: Registrando {x+1} de {total}{CR_LF}".encode())
            time.sleep(0.5)
