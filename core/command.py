import time
import board
import digitalio

CR_LF = f"\n\r"

# Definir estados posibles
ESTADO_INICIO = 0
ESTADO_ESPERANDO_COMANDO = 1
ESTADO_ESPERANDO_PARAMETROS = 2
ESTADO_ESPERANDO_ENTER = 3

class Command:
    def __init__(self, serial):
        self.serial = serial
        self.estado_actual = ESTADO_INICIO
        self.led = digitalio.DigitalInOut(board.D13)
        self.led.direction = digitalio.Direction.OUTPUT
        self.inicio = 0
        self.func = None
        self.func_code = None
        self.buffer_parametros = ""

        self.comandos = {
            "?": (self.mostrar_ayuda, 0),
            "R": (self.iniciar_registro, 2),
        }

    def mostrar_ayuda(self):
        self.serial.write(f"Comandos disponibles:{CR_LF}".encode())
        self.serial.write(f"ESC ?{CR_LF}".encode())
        self.serial.write(f"ESC R <num>,<total>{CR_LF}".encode())

    def iniciar_registro(self, num, total):
        for x in range(total):
            self.serial.write(f"{num}: Registrando {x+1} de {total}{CR_LF}".encode())
            time.sleep(0.5)

    def espera_comando(self):
        if self.serial.in_waiting > 0:
            char = self.serial.read(1).decode()
            self.procesar_char(char)
            if self.estado_actual != ESTADO_INICIO:
                self.inicio = time.monotonic()
                self.led.value = True

        if time.monotonic() - self.inicio >= 1:
            self.led.value = False
            self.estado_actual = ESTADO_INICIO
            self.buffer_parametros = ""

    def procesar_char(self, char):
        if self.estado_actual == ESTADO_INICIO:
            if char == "\x1b":
                self.estado_actual = ESTADO_ESPERANDO_COMANDO

        elif self.estado_actual == ESTADO_ESPERANDO_COMANDO:
            if char in self.comandos:
                self.func, self.args_esperados = self.comandos[char]
                self.func_code = char
                if self.args_esperados > 0:
                    self.buffer_parametros = ""
                    self.estado_actual = ESTADO_ESPERANDO_PARAMETROS
                else:
                    self.estado_actual = ESTADO_ESPERANDO_ENTER

        elif self.estado_actual == ESTADO_ESPERANDO_PARAMETROS:
            if char == "\x0d":
                parametros = [p.strip() for p in self.buffer_parametros.split(",") if p.strip() != ""]

                if len(parametros) != self.args_esperados:
                    self.serial.write(f"Error: Se esperaban {self.args_esperados} parámetros, pero se recibieron {len(parametros)}{CR_LF}".encode())
                else:
                    try:
                        parametros = [int(p) for p in parametros]
                        self.func(*parametros)
                    except ValueError:
                        self.serial.write(f"{self.func_code}: Parámetros deben ser números enteros{CR_LF}".encode())

                self.buffer_parametros = ""
                self.estado_actual = ESTADO_INICIO
            else:
                self.buffer_parametros += char

        elif self.estado_actual == ESTADO_ESPERANDO_ENTER:
            if char == "\x0d":
                if self.func is not None:
                    self.func()
                    self.func = None

                self.estado_actual = ESTADO_INICIO
                self.led.value = False


