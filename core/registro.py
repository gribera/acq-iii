import asyncio

class Registro:
    def __init__(self, serial):
        self.serial = serial

    async def iniciar_registro(self, num, total):
        for x in range(total):
            self.serial.write(f"{num}: Registrando {x+1}/{total}\n\r".encode())
            await asyncio.sleep(0.5)