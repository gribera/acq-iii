from core.registro import Registro

def show_help(cmd, serial):
    CR_LF = "\n\r"
    serial.write(f"Comandos disponibles:{CR_LF}".encode())
    serial.write(f"ESC ?{CR_LF}".encode())
    serial.write(f"ESC R <num>,<total>{CR_LF}".encode())

def run_iniciar_registro(cmd, serial, num, total):
    if not hasattr(cmd, 'data_logger'):
        cmd.data_logger = Registro(serial)
    cmd.data_logger.iniciar_registro(num, total)

COMANDOS = {
    "?": (show_help, 0),
    "R": (run_iniciar_registro, 2),
}
