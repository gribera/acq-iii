import time
import board
import digitalio
from core.comandos import COMANDOS
from config import COMANDO_INICIO, TIMEOUT_COMANDOS

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
        self.func_code = None
        self.buffer_parametros = ""
        self.func = None
        self.args_esperados = 0

    def espera_comando(self):
        if self.serial.in_waiting > 0:
            char = self.serial.read(1).decode()
            self.__procesar_char(char)
            if self.estado_actual != ESTADO_INICIO:
                self.inicio = time.monotonic()
                self.led.value = True

        if time.monotonic() - self.inicio >= TIMEOUT_COMANDOS:
            self.__finalizar_recepcion()

    def __procesar_char(self, char):
        if self.estado_actual == ESTADO_INICIO:
            if char == COMANDO_INICIO:
                self.estado_actual = ESTADO_ESPERANDO_COMANDO

        elif self.estado_actual == ESTADO_ESPERANDO_COMANDO:
            if char in COMANDOS:
                self.func, self.args_esperados = COMANDOS[char]
                self.func_code = char
                if self.args_esperados > 0:
                    self.buffer_parametros = ""
                    self.estado_actual = ESTADO_ESPERANDO_PARAMETROS
                else:
                    self.estado_actual = ESTADO_ESPERANDO_ENTER
            else:
                self.estado_actual = ESTADO_ESPERANDO_ENTER

        elif self.estado_actual == ESTADO_ESPERANDO_PARAMETROS:
            if char == "\x0d":
                parametros = [p.strip() for p in self.buffer_parametros.split(",") if p.strip() != ""]

                if len(parametros) != self.args_esperados:
                    self.serial.write(f"Error: Se esperaban {self.args_esperados} parámetros, pero se recibieron {len(parametros)}\n\r".encode())
                else:
                    try:
                        parametros = [int(p) for p in parametros]
                        self.parametros_actuales = parametros
                        if self.func is not None:
                            self.func(self, self.serial, *parametros)
                    except ValueError:
                        self.serial.write(f"{self.func_code}: Parámetros deben ser números enteros\n\r".encode())

                self.__finalizar_recepcion()
            else:
                self.buffer_parametros += char

        elif self.estado_actual == ESTADO_ESPERANDO_ENTER:
            if char == "\x0d":
                if self.func is not None:
                    self.func(self, self.serial)
                self.__finalizar_recepcion()

    def __finalizar_recepcion(self):
        self.estado_actual = ESTADO_INICIO
        self.led.value = False
        self.buffer_parametros = ""
        self.func = None


