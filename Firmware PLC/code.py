import board
import digitalio
import analogio
import time
import gc
import re

# --- LIBRERÍA DE BLOQUES Y FUNCIONES IEC 61131-3 ---
# Estos objetos tienen memoria. Recuerdan lo que pasó en el ciclo anterior.
def MOVE(EN, IN):
    """Implementación de MOVE: Retorna (Valor, ENO)"""
    if EN:
        return IN, True
    return 0, False

class R_TRIG:
    def __init__(self):
        self.CLK, self.Q = False, False
    def update(self, CLK=False):
        self.Q = CLK and not self.CLK
        self.CLK = CLK
        return self.Q

class F_TRIG:
    def __init__(self):
        self.CLK, self.Q = False, False
    def update(self, CLK=False):
        self.Q = not CLK and self.CLK
        self.CLK = CLK
        return self.Q

class TON:
    def __init__(self):
        self.IN, self.Q, self.PT, self.ET = False, False, 0.0, 0.0
        self._start_time = None
    def update(self, IN=False, PT=0.0):
        self.PT = PT
        if not IN:
            self.Q, self.ET, self._start_time = False, 0.0, None
        else:
            if self._start_time is None: self._start_time = time.monotonic()
            self.ET = time.monotonic() - self._start_time
            if self.ET >= self.PT:
                self.Q, self.ET = True, self.PT
        return self.Q

class CTU:
    def __init__(self):
        self.CV, self.Q, self.last_CU = 0, False, False
    def update(self, CU=False, PV=0, R=False):
        if R: self.CV = 0
        elif CU and not self.last_CU: self.CV += 1
        self.Q = self.CV >= PV
        self.last_CU = CU
        return self.Q

class RS:
    def __init__(self): self.Q1 = False
    def update(self, S=False, R1=False):
        if R1: self.Q1 = False
        elif S: self.Q1 = True
        return self.Q1

class SR:
    def __init__(self): self.Q1 = False
    def update(self, S1=False, R=False):
        if S1: self.Q1 = True
        elif R: self.Q1 = False
        return self.Q1

# --- MOTOR PLC GCM4 ULTRA ---

class PLC_GCM4_Ultra:
    def __init__(self, st_file):
        self.pins = {} # aca se almacenan objetos de hardware (DigitalInOut, analogIn)
        self.blocks = {} #aca se almacenan las instancias CTU,TON, etc
        self.logic = [] # Acá se guarda el código traducido
        self.hw_map = {  #acá se vinculan las direcciones IEC con pines físicos de la GCM4
            "%IX0.1": board.D2, "%IX0.2": board.D3, "%IX0.3": board.D4, "%IX0.4": board.D5,
            "%QX0.1": board.D13, "%QX0.2": board.D12, "%QX0.3": board.D14,
            "%IW0": board.A0, "%IW1": board.A1,
            "%QW0": board.A2
        }
        self.parse(st_file)

    def parse(self, filename):
        print(f"Analizando programa IEC: {filename}")
        indent_level = 0
        with open(filename, "r") as f:
            for line in f:
                # Limpieza de comentarios y puntos y coma
                l = line.strip().split("//")[0].split("(*")[0].replace(";", "")
                if not l or any(x in l for x in ("PROGRAM", "CONFIGURATION", "RESOURCE", "TASK")):
                    continue

                # Gestión de bloques VAR y Programa
                if any(x in l for x in ("VAR", "END_VAR", "END_PROGRAM", "END_RESOURCE", "END_CONFIGURATION")):
                    continue

                # Manejo de fin de condicionales para indentación
                if "END_IF" in l:
                    indent_level = max(0, indent_level - 1)
                    continue

                try:
                    prefix = "    " * indent_level

                    # 1. Configuración de Hardware (Direccionamiento AT) [cite: 2]
                    if " AT " in l:
                        parts = l.split()
                        name, addr = parts[0], parts[2]
                        if addr in self.hw_map:
                            pin = self.hw_map[addr]
                            if "%QW" in addr:
                                self.pins[name] = analogio.AnalogOut(pin)
                            elif "%IW" in addr:
                                self.pins[name] = analogio.AnalogIn(pin)
                            elif "%IX" in addr:
                                io = digitalio.DigitalInOut(pin)
                                io.direction = digitalio.Direction.INPUT
                                io.pull = digitalio.Pull.UP
                                self.pins[name] = io
                            else:
                                io = digitalio.DigitalInOut(pin)
                                io.direction = digitalio.Direction.OUTPUT
                                self.pins[name] = io
                        continue

                    # 2. Instanciación de Bloques Funcionales (CTU, TON, etc.) [cite: 1]
                    if ":" in l and ":=" not in l and "(" not in l:
                        name, b_type = [x.strip() for x in l.split(":")]
                        types = {"CTU": CTU, "R_TRIG": R_TRIG, "F_TRIG": F_TRIG, "TON": TON, "RS": RS, "SR": SR}
                        if b_type in types:
                            self.blocks[name] = types[b_type]()
                        continue

                    # 3. Estructuras Condicionales IF...THEN
                    if l.startswith("IF ") and " THEN" in l:
                        cond = l.replace("IF ", "").replace(" THEN", "").strip()
                        cond = cond.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                        self.logic.append(f"{prefix}if {cond}:")
                        indent_level += 1
                        continue

                    # 4. Función MOVE con soporte para ENO =>
                    if "MOVE(" in l:
                        target, rest = l.split(":=", 1)
                        # Detectar asignación de ENO
                        eno_match = re.search(r"ENO\s*=>\s*(\w+)", rest)
                        eno_var = eno_match.group(1) if eno_match else None
                        # Extraer y limpiar parámetros
                        params = re.search(r"\((.*)\)", rest).group(1)
                        if "ENO" in params: params = params.split(", ENO")[0]
                        params = params.replace(":=", "=").replace("AND", " and ").replace("OR", " or ")

                        self.logic.append(f"{prefix}res, eno = MOVE({params})")
                        self.logic.append(f"{prefix}{target.strip()} = res")
                        if eno_var: self.logic.append(f"{prefix}{eno_var} = eno")
                        continue

                    # 5. Llamadas a Bloques Funcionales (ej: CTU0(CU:=...)) [cite: 1]
                    block_call_match = re.match(r"(\w+)\s*\((.*)\)", l)
                    if block_call_match:
                        b_name = block_call_match.group(1)
                        if b_name in self.blocks:
                            params = block_call_match.group(2).replace(":=", "=")
                            # Convertir T# a segundos
                            params = re.sub(r"T#(\d+)ms", lambda m: str(float(m.group(1))/1000.0), params)
                            params = re.sub(r"T#(\d+)s", lambda m: m.group(1), params)
                            self.logic.append(f"{prefix}{b_name}.update({params})")
                            continue

                    # 6. Asignaciones Estándar
                    if ":=" in l:
                        target, expr = [x.strip() for x in l.split(":=", 1)]
                        expr = expr.replace("NOT", "not").replace("AND", " and ").replace("OR", " or ")
                        self.logic.append(f"{prefix}{target} = {expr}")

                except Exception as e:
                    print(f"Error parseando línea: {l} -> {e}")

    def run(self):
        ctx = {"MOVE": MOVE}
        print("GCM4 PLC: RUNNING...")
        compiled_logic = "\n".join(self.logic)

        while True:
            # Ciclo de lectura
            for name, io in self.pins.items():
                if isinstance(io, analogio.AnalogIn):
                    ctx[name] = (io.value / 65535) * 100.0
                elif isinstance(io, digitalio.DigitalInOut) and io.direction == digitalio.Direction.INPUT:
                    ctx[name] = not io.value

            # Cargar bloques en contexto
            for b_name, b_obj in self.blocks.items():
                ctx[b_name] = b_obj

            # Ejecutar lógica compilada
            try:
                exec(compiled_logic, ctx)
            except Exception as e:
                # Opcional: print(f"Runtime Error: {e}")
                pass

            # Ciclo de escritura
            for name, io in self.pins.items():
                if name in ctx:
                    if isinstance(io, analogio.AnalogOut):
                        val = int(min(65535, max(0, ctx[name])))
                        io.value = val
                    elif isinstance(io, digitalio.DigitalInOut) and io.direction == digitalio.Direction.OUTPUT:
                        io.value = ctx[name]

            time.sleep(0.01)

# --- LANZAMIENTO ---
try:
    plc = PLC_GCM4_Ultra("program.st")
    plc.run()
except Exception as e:
    print(f"Critical PLC Crash: {e}")