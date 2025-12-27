import json
from pyladdersim.components import Contact, InvertedContact, Output
from pyladdersim.ladder import Rung, Ladder

# 1. Definir componentes (Asegúrate de que el 'name' coincida con tu hardware.py)
input1 = Contact(name="I0.0")        # Start
input2 = InvertedContact(name="I0.1") # Stop
output = Output(name="Q0.0")         # Lamp

# 2. Crear renglón y escalera
rung1 = Rung([input1, input2, output])
ladder = Ladder()
ladder.add_rung(rung1)

# --- NUEVA FUNCIÓN DE EXPORTACIÓN ---
def exportar_json(ladder_obj, filename="project.json"):
    data = {"rungs": []}
    for r in ladder_obj.rungs:
        elementos = []
        for comp in r.components:
            if comp != r.output: # No incluimos la salida en la lista de condiciones
                # Detectamos el tipo de contacto para el JSON
                tipo = "NC" if isinstance(comp, InvertedContact) else "NO"
                elementos.append({"type": tipo, "address": comp.name})
        
        data["rungs"].append({
            "elements": elementos,
            "output_address": r.output.name
        })
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Archivo {filename} generado para la Grand Central M4.")

# 3. Guardar el archivo antes de correr la simulación
exportar_json(ladder)

# 4. (Opcional) Correr la visualización en PC
# ladder.run(visualize=True)