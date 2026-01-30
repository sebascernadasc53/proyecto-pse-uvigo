print("Programa orbita")
from motor import Ordinary_Car
from ultrasonic import Ultrasonic
import time

# Inicialización
ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
d_target = 40
tolerancia = 5
try:
    while True:
        distance = ultrasonic.get_distance()
        if distance is not None:
            print(f"Distancia ultrasonidos {distance} cm")
        if distance > d_target:
            print("Buscando objeto que orbitar")
            PWM.set_motor_model(600,600,600,600)
        if distance < d_target:
            print ("Stopping")
            PWM.set_motor_model(0,0,0,0)
            time.sleep(0.5)

            print("Identificando objeto")
            d0 = ultrasonic.get_distance()

            print("Probando orbita horaria...")
            PWM.set_motor_model(0,0,-600,600) #orbita horario
            time.sleep(1.5)# tiempo de orbita de testeo
            PWM.set_motor_model(0,0,0,0)
            d1 = ultrasonic.get_distance()
            delta1 = abs(d1-d0)
            print(f"variacion {delta1} cm")

            print("Probando orbita antihoraria...")
            PWM.set_motor_model(0,0,+600,-600) #orbita horario
            time.sleep(1.5)# tiempo de orbita de testeo
            PWM.set_motor_model(0,0,0,0)
            d2 = ultrasonic.get_distance()
            delta2 = abs(d2-d0)
            print(f"variacion {delta2} cm")

            if delta1 < tolerancia or delta2 < tolerancia:
                print("Orbitable, comenzando órbita")
                PWM.set_motor_model(0,0,+600,-600)
            else:
                print("No orbitable")
except KeyboardInterrupt:
    PWM.set_motor_model(0,0,0,0)
    print("Programa detenido")
