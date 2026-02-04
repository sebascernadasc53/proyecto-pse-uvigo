import time
from motor import Ordinary_Car 
from ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()
PWM = Ordinary_Car()

D_TARGET = 40  # Distancia deseada al objeto (cm)
TOL= 5
SPEED = 800
def verificar_objeto():
    print("Analizando orbitabilidad...")
    lecturas = []
    for _ in range (5):
        d = ultrasonic.get_distance()
        if d: lecturas.append(d)
        time.sleep(0.1)
    if len(lecturas) < 3:
        print(f"No hay suficientes lecturas {(len(lecturas))} para verificar el objeto")
        return False
    


def stop_robot():
    PWM.set_motor_model(0, 0, 0, 0)

try:
    while True:
        dist = ultrasonic.get_distance()
        
        if dist is None:
            continue

        print(f"Distancia: {dist} cm")

        if dist > D_TARGET + TOL:
            print("Buscando objeto...")
            PWM.set_motor_model(-SPEED,-SPEED, -SPEED, -SPEED)

        elif dist < D_TARGET:

            print("Demasiado cerca, alejándose")
            PWM.set_motor_model(SPEED, SPEED, SPEED, SPEED)
            
        else:

            print("Deteniendo para verificar...")
# verificacion
            if verificar_objeto():
                print("Objeto orbitable. Iniciando órbita...")
                # Movimiento Mecanum: Strafe lateral + corrección de ángulo
                while True:
                    d_actual = ultrasonic.get_distance()
                    if d_actual is None or d_actual > D_TARGET + 20:
                        print("Objeto perdido durante la órbita")
                        break
                    
                    # Órbita sentido horario
                    # Ajustar valores segun respuesta del robot
                    PWM.set_motor_model(SPEED, -SPEED//2, -SPEED//2, SPEED)
            else:
                print("Objeto inestable o demasiado pequeño. Reintentando...")
                # Pequeño giro para buscar por otro lado
                PWM.set_motor_model(500, 500, -500, -500)
                time.sleep(0.3)

except KeyboardInterrupt:
    PWM.set_motor_model(0,0,0,0)
    print("Programa detenido")
            