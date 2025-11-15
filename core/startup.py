from core.memory import MemoryService
from core.wifi import get_wifi

from config import (MEMORIAS,
                    STARTUP_DATA_STORAGE,
                    STARTUP_SEQUENCE_BYTE,
                    STARTUP_SERVICES)


class StartupService:
    def __init__(self):
        mem = MemoryService()
        self._sequence = mem.read_string(MEMORIAS[STARTUP_DATA_STORAGE],
                                     STARTUP_SEQUENCE_BYTE,
                                     1)
        mem.close()

    def get_startup_info(self):
        """
        Lista los servicios que existen para ejecución al inicio

        Returns:
            None
        """
        seq = self._sequence.encode()[0]

        print("Servicios de arranque:")
        for cod_service, (service, bit) in STARTUP_SERVICES.items():
            enabled = bool((seq >> bit) & 1)
            print(f"{bit} - {service} ({cod_service}): {"Habilitado" if enabled else "Deshabilitado"}")

    def toggle_startup_service(self, cod_service: str):
        """
        Habilita/Deshabilita servicios para ejecución al inicio.

        Args:
            cod_service (str): Servicio a habilitar/deshabilitar

        Returns:
            None
        """
        print("[Startup]", end=" ")
        if cod_service not in STARTUP_SERVICES:
            print(f"Servicio desconocido: {cod_service}")
            return

        (service, bit) = STARTUP_SERVICES[cod_service]
        mask = 1 << bit

        seq = self._sequence.encode()[0]

        # Toggle del bit
        seq ^= mask

        # Guardar nuevo valor
        self._sequence = bytes([seq]).decode()
        mem = MemoryService()
        mem.write_string(MEMORIAS[STARTUP_DATA_STORAGE],
                                     STARTUP_SEQUENCE_BYTE,
                                     self._sequence)
        mem.close()

        enabled = bool((seq >> bit) & 1)
        print(f"{service}: {"Habilitado" if enabled else "Deshabilitado"}.")

    def exec_startup(self):
        """
        Recorre todos los servicios y ejecuta los que están habilitados

        Returns:
            None
        """
        print("Iniciando...")
        seq = self._sequence.encode()[0]
        for cod_service, (service, bit) in STARTUP_SERVICES.items():
            enabled = bool((seq >> bit) & 1)

            if cod_service == "w" and enabled:
                wifi = get_wifi()
                wifi.connect()
