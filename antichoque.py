import time
from threading import Thread
from robot import Robot

# Inicialización
rover1 = Robot()
dist = 0
v=1000

print("Prueba...")

try:
    while True:
        dist = rover1.distance
        
        if dist > 90:
            v=v
        elif 25 < dist <= 90:
            v=0.6*v
        else:
            print(f"¡Objeto detectado! Frenando...")
            v=0
            
        rover1.motores(v)
        print(f"d={dist} cm")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nFinalizando ejecución...")
finally:
    rover1.finalizar()