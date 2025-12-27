import json
# Importamos las clases de tu repositorio local
from pyladdersim.components import Contact, Output
from pyladdersim.ladder import Rung, Ladder

def generar_ejemplo_simple():
    # 1. Crear componentes (usa las direcciones que definimos en el hardware_map)
    boton_start = Contact("I0.0") # Contacto Normalmente Abierto
    led_indicador = Output("Q0.0") # Salida física
    
    # 2. Crear un renglón (Rung)
    # Un renglón es una lista donde el último elemento es la salida
    renglon1 = Rung([boton_start, led_indicador])
    
    # 3. Empaquetar en la estructura JSON
    # Este formato coincide con el intérprete que cargamos en la GCM4
    data_proyecto = {
        "rungs": [
            {
                "elements": [
                    {"type": "NO", "address": "I0.0"}
                ],
                "output_address": "Q0.0"
            }
        ]
    }
    
    # 4. Guardar el archivo
    with open("project.json", "w") as f:
        json.dump(data_proyecto, f, indent=4)
    
    print("✅ Archivo 'project.json' creado con éxito.")
    print("Contenido lógico: Si I0.0 (D2) está presionado -> Activa Q0.0 (D13)")

if __name__ == "__main__":
    generar_ejemplo_simple()