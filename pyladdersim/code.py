import board
import digitalio
import json
import time

# --- DICCIONARIO DE PINES ---
# Mapeamos los nombres del JSON a objetos de hardware reales
pin_map = {
    "D2": board.D2,
    "D3": board.D3,
    "D13": board.D13,
    # Agrega aquí los pines que necesites de tu Grand Central
}

# --- CLASE MOTOR DE ESCALERA ---
class LadderInterpreter:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.data = json.load(f)
        self.pins = {}
        self.setup_hw()

    def setup_hw(self):
        # Configurar entradas y salidas según el JSON
        for rung in self.data["rungs"]:
            for inp in rung["inputs"]:
                name = inp["pin"]
                if name not in self.pins:
                    p = digitalio.DigitalInOut(pin_map[name])
                    p.direction = digitalio.Direction.INPUT
                    p.pull = digitalio.Pull.UP # Asumimos botones a GND
                    self.pins[name] = p
            
            out_name = rung["output"]
            if out_name not in self.pins:
                p = digitalio.DigitalInOut(pin_map[out_name])
                p.direction = digitalio.Direction.OUTPUT
                self.pins[out_name] = p

    def run_cycle(self):
        for rung in self.data["rungs"]:
            # Lógica AND por defecto para los elementos de un renglón
            resultado_renglon = True
            for inp in rung["inputs"]:
                valor_real = self.pins[inp["pin"]].value
                # Si es Normalmente Abierto (NO), invertimos porque usamos Pull.UP
                estado_contacto = not valor_real if inp["type"] == "NO" else valor_real
                resultado_renglon = resultado_renglon and estado_contacto
            
            # Actualizar la bobina (salida)
            self.pins[rung["output"]].value = resultado_renglon

# --- INSTANCIA Y BUCLE ---
mi_plc = LadderInterpreter("logic.json")

print("PLC Virtual iniciado en Grand Central M4...")

while True:
    mi_plc.run_cycle()
    time.sleep(0.01) # Tiempo de scan de 10ms