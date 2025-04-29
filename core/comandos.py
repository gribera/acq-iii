from core.registro import Registro

async def show_help(cmd, serial):
    serial.write(f"Comandos disponibles:\n\r".encode())
    serial.write(f"ESC ?\n\r".encode())
    serial.write(f"ESC R <num>,<total>\n\r".encode())

async def run_iniciar_registro(cmd, serial, num, total):
    cmd.data_logger = Registro(serial)
    await cmd.data_logger.iniciar_registro(num, total)

COMANDOS = {
    "?": (show_help, 0),
    "R": (run_iniciar_registro, 2),
}