from motor import Ordinary_Car
from ultrasonic import Ultrasonic
import time
from threading import Thread

# Inicialización
ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
distance = 0
running = True  # Flag de control global

def leer_ultrasonidos():
    global distance
    while running: # El hilo se detiene si running es False
        distance = ultrasonic.get_distance()
        if distance is not None:
            print(f"Distancia ultrasonidos {distance} cm")
        time.sleep(0.05) # Evita saturar el bus

def motores():
    while running: # El hilo se detiene si running es False
        if distance > 90:
            PWM.set_motor_model(-4095, -4095, -4095, -4095) # mínimo para que arranque 600
        elif 25 < distance <= 90:
            PWM.set_motor_model(-400, -400, -400, -400)
        else:
            PWM.set_motor_model(0, 0, 0, 0)
        time.sleep(0.05) # Crucial para soltar el GIL y permitir el cierre

try: 
    sensor_thread = Thread(target=leer_ultrasonidos, daemon=True)
    motor_thread = Thread(target=motores, daemon=True)

    sensor_thread.start()
    motor_thread.start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Deteniendo sistemas...")
    running = False  # 1. Ordenamos a los hilos detener sus bucles
    time.sleep(0.2)  # 2. Esperamos un instante a que los hilos terminen
    PWM.set_motor_model(0, 0, 0, 0) # 3. Enviamos la orden final de parada

finally:
    running = False
    PWM.set_motor_model(0, 0, 0, 0)
    # Intentar limpiar la librería si tiene el método
    if hasattr(PWM, 'close'):
        PWM.close()
    print("Programa finalizado con éxito.")