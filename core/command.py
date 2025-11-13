import asyncio
import time
import board
import digitalio
from core.comandos import COMANDOS
from config import COMANDO_INICIO, COMANDO_FIN, TIMEOUT_COMANDOS

ESTADO_INICIO = 0
ESTADO_ESPERANDO_COMANDO = 1
ESTADO_ESPERANDO_SUBCOMANDO = 2
ESTADO_ESPERANDO_PARAMETROS = 3
ESTADO_ESPERANDO_ENTER = 4

class Command:
    def __init__(self, serial):
        self.serial = serial
        self.estado_actual = ESTADO_INICIO
        self.led = digitalio.DigitalInOut(board.D13)
        self.led.direction = digitalio.Direction.OUTPUT
        self.inicio = 0
        self.func_code = None
        self.sub_code = None
        self.buffer_parametros = ""
        self.func = None
        self.args_esperados = 0

    async def espera_comando(self):
        """ Espera comando para ser procesado por la máquina de estados """
        while self.serial.in_waiting > 0:
            char = self.serial.read(1).decode()
            await self._procesar_char(char)
            if self.estado_actual != ESTADO_INICIO:
                self.inicio = time.monotonic()
                self.led.value = True

        if time.monotonic() - self.inicio >= TIMEOUT_COMANDOS:
            self._finalizar_recepcion()

    async def _procesar_char(self, char):
        if self.estado_actual == ESTADO_INICIO:
            if char == COMANDO_INICIO:
                self.estado_actual = ESTADO_ESPERANDO_COMANDO

        elif self.estado_actual == ESTADO_ESPERANDO_COMANDO:
            if char in COMANDOS:
                comando = COMANDOS[char]
                self.func_code = char
                if isinstance(comando, dict):
                    # Tiene subcomandos
                    self.comando_actual = comando
                    self.estado_actual = ESTADO_ESPERANDO_SUBCOMANDO
                else:
                    self.func, self.args_esperados = comando
                    self.estado_actual = (
                        ESTADO_ESPERANDO_PARAMETROS if self.args_esperados > 0
                        else ESTADO_ESPERANDO_ENTER
                    )
            else:
                self.estado_actual = ESTADO_ESPERANDO_ENTER

        elif self.estado_actual == ESTADO_ESPERANDO_SUBCOMANDO:
            if char in self.comando_actual:
                self.func, self.args_esperados = self.comando_actual[char]
                self.sub_code = char
                if self.args_esperados > 0:
                    self.buffer_parametros = ""
                    self.estado_actual = ESTADO_ESPERANDO_PARAMETROS
                else:
                    self.estado_actual = ESTADO_ESPERANDO_ENTER
            else:
                # Evita que se muestre el mensaje cuando el usuario presiona ENTER sin subcomando
                if char != COMANDO_FIN:
                    self.serial.write(f"Subcomando '{char}' no válido\r\n".encode())
                self._finalizar_recepcion()

        elif self.estado_actual == ESTADO_ESPERANDO_PARAMETROS:
            if char == COMANDO_FIN:
                parametros = [p.strip() for p in self.buffer_parametros.split(",") if p.strip() != ""]
                if len(parametros) != self.args_esperados:
                    self.serial.write(
                        f"Error: Se esperaban {self.args_esperados} parámetros, pero se recibieron {len(parametros)}\r\n".encode()
                    )
                else:
                    try:
                        # Permitimos strings si no son solo dígitos
                        casted = [int(p) if p.isdigit() else p for p in parametros]
                        asyncio.create_task(self.func(self, self.serial, *casted))
                    except Exception as e:
                        self.serial.write(f"Error ejecutando comando: {e}\r\n".encode())
                self._finalizar_recepcion()
            else:
                self.buffer_parametros += char

        elif self.estado_actual == ESTADO_ESPERANDO_ENTER:
            if char == COMANDO_FIN:
                if self.func:
                    asyncio.create_task(self.func(self, self.serial))
                self._finalizar_recepcion()
    def _finalizar_recepcion(self):

        self.estado_actual = ESTADO_INICIO
        self.led.value = False
        self.buffer_parametros = ""
        self.func = None
