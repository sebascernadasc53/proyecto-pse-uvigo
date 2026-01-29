from motor import Ordinary_Car
from ultrasonic import Ultrasonic
import time
from threading import Thread

# Inicialización
ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
distance = 0  # Variable global para compartir entre hilos

def leer_ultrasonidos():
    global distance
    while True:
        lectura = ultrasonic.get_distance()
        if lectura is not None:
            distance = lectura
            print(f"Distancia: {distance} cm")

def motores():
    while True:
        if distance > 80:
            PWM.set_motor_model(-800, -800, -800, -800) # Avance rápido
            print("Estado: Avanzando rápido")
        elif 25 < distance <= 80:
            PWM.set_motor_model(-400, -400, -400, -400)     # Avance lento
            print("Estado: Reduciendo velocidad")
        elif distance <=25:
            PWM.set_motor_model(0, 0, 0, 0)                 # Stop
            print("Estado: PARADO (Obstáculo)")
        else:
            PWM.set_motor_model(0, 0, 0, 0)                 # Stop
            print("Estado: PARADO (Obstáculo)")
        

try: 
    # Creamos los hilos una sola vez
    sensor_thread = Thread(target=leer_ultrasonidos, daemon=True)
    motor_thread = Thread(target=motores, daemon=True)

    # Iniciamos los hilos
    sensor_thread.start()
    motor_thread.start()

    # Mantenemos el programa principal vivo
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDeteniendo robot...")
    PWM.set_motor_model(0, 0, 0, 0) # Asegurar que pare al salir
finally:
    PWM.set_motor_model(0, 0, 0, 0)
    time.sleep(1)                 # Stop
    ultrasonic.close()
    PWM.close()
    print("Programa finalizado")