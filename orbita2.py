import time
from motor import Ordinary_Car 
from ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()
PWM = Ordinary_Car()

D_TARGET = 40  # Distancia deseada al objeto (cm)
TOL = 5
Speed = [-400,4000,400,-4000]
def verificar_objeto():
    print("Analizando orbitabilidad...")
    lecturas = []
    for _ in range (5):
        PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3]) #orbita
        time.sleep(0.3)
        d = ultrasonic.get_distance()
        if d: lecturas.append(d)
        time.sleep(0.5)
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
        d = ultrasonic.get_distance()
        PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3])
        if d >=D_TARGET + 2*TOL or d < D_TARGET - 2*TOL:
            print("Órbita perdida")
            PWM.set_motor_model(0,0,0,0)
            break
        
try: #bucle principal, buscar objeto
    while True:
        d = ultrasonic.get_distance()
        if d > D_TARGET + TOL:
            PWM.set_motor_model(-1000,-1000,-1000,-1000)
            print("Buscando objetivo")
        elif d < D_TARGET - TOL:
            PWM.set_motor_model(1000,1000,1000,1000)
            print("Demasiado cerca, retrocediendo")
        else:
            if verificar_objeto():
                orbitar_objeto()
except KeyboardInterrupt:
    print("Abortando programa")
    PWM.set_motor_model(0,0,0,0)