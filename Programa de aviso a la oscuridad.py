from buzzer import Buzzer
from adc import ADC
import time

#Inicialización de componentes
bocina = Buzzer()
adc = ADC()

#Definimos un Umbral de 1.2, por ejemplo
UMBRAL = 1.2

try:
    print("Inicio del sistema de alerta por oscuridad (antipérdida del vehículo)...")
    while True:
        # Leemos los valores que dan los sensores de los sensores de luz
        val_izq = adc.read_adc(0)
        val_der = adc.read_adc(1)

        if val_izq is not None and val_der is not None:
            print(f"Valor de sensor izquierdo: {val_izq}V | Valor de sensor derecho: {val_der}V")

            # Si alguno de los dos sensores está en la oscuridad, se activa la bocina
            if val_izq <= UMBRAL or val_der <= UMBRAL:
                bocina.set_state(True) # Se enciende la bocina
                print("Zona oscura detectada: Bocina activa")
            else:
                bocina.set_state(False) # Se apaga la bocina
                print("Luz suficiente. Sin peligro de pérdida")
        else:
            print("Posible fallo de lectura: comprobar conexión y estado de cables")
            bocina.set_state(False) # Apagamos la bocina en caso de fallo

        time.sleep(0.5) # time sleep para cada ciclo de medida

except KeyboardInterrupt: # Cierre de programa
    print("\nDeteniendo programa...")
    bocina.set_state(False) # Nos aseguramos de apagar la bocina

finally:
    # Cerramos la bocina y el sensor_luz
    bocina.close()
    print("Fin de programa de búsqueda")