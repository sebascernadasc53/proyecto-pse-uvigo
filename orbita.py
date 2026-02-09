import time
from motor import Ordinary_Car 
from ultrasonic import Ultrasonic
from threading import Thread

ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
distance = 0.0
D_TARGET = 40  # Distancia deseada al objeto (cm)
TOL = 5
Speed = [-400,4000,400,-4000]
running = True

 # HILO SENSOR
def sensor_thread():
    global distance
    while running:
        lectura = ultrasonic.get_distance()
        if lectura is not None:
            distance = lectura
        time.sleep(0.05)
def verificar_objeto():
    print("Analizando orbitabilidad...")
    lecturas = []
    for _ in range (5):
        PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3]) #orbita
        time.sleep(0.3)
        lecturas.append(distance)
        time.sleep(0.2)
    if len(lecturas) < 3:
        print(f"No hay suficientes lecturas, {(len(lecturas))},para verificar el objeto")
        return False
    elif max(lecturas) >=D_TARGET + TOL or min(lecturas) < D_TARGET - TOL:
        print("No orbitable")
        return False
    else:
        print("Orbitable")
        return True
def orbitar_objeto():
    while True:
        PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3])
        if distance >=D_TARGET + 2*TOL or distance < D_TARGET - 2*TOL:
            print("Órbita perdida")
            PWM.set_motor_model(0,0,0,0)
            break
        time.sleep(0.1)

t = Thread(target=sensor_thread)
t.daemon = True
t.start()

#bucle principal, buscar objeto
try:
    while True:

        if distance > D_TARGET + TOL:
            PWM.set_motor_model(-1000,-1000,-1000,-1000)
            print("Buscando objetivo")
        elif distance < D_TARGET - TOL:
            PWM.set_motor_model(1000,1000,1000,1000)
            print("Demasiado cerca, retrocediendo")
        else:
            if verificar_objeto():
                orbitar_objeto()
except KeyboardInterrupt:
    running = False
    print("Abortando programa")
    PWM.set_motor_model(0,0,0,0)