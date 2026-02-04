import time
from threading import Thread
from robot import Robot

# Inicialización
rover1 = Robot()
dist = 0
v0=1000

print("Prueba...")

try:
    while True:
        dist = rover1.distance
        
        if dist > 90:
            v=v0
            print(f"d={dist} cm Movimiento")
        elif 25 < dist <= 90:
            v=0.6*v0
            print(f"d={dist} cm Movimiento")
        else:
            print(f"d={dist} cm ¡Objeto detectado! Frenando...")
            v=0
            
        rover1.motores(int(-v))
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nFinalizando ejecución...")
finally:
    rover1.finalizar()