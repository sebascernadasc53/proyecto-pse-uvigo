import time
from motor import Ordinary_Car # Asegúrate de que esta clase soporte 4 argumentos
from ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()
robot = Ordinary_Car()

D_TARGET = 40  # Distancia deseada al objeto (cm)
TOLERANCIA = 5
SPEED = 800

def stop_robot():
    robot.set_motor_model(0, 0, 0, 0)

try:
    while True:
        dist = ultrasonic.get_distance()
        
        if dist is None:
            continue

        print(f"Distancia: {dist} cm")

        if dist > D_TARGET + 20:
            # Si está muy lejos, avanza de frente
            print("Buscando objeto...")
            robot.set_motor_model(SPEED, SPEED, SPEED, SPEED)
        
        elif dist < D_TARGET - 10:
            # Si está demasiado cerca, retrocede un poco
            print("Demasiado cerca, alejándose")
            robot.set_motor_model(-SPEED, -SPEED, -SPEED, -SPEED)
            
        else:
            # RANGO DE ÓRBITA: Desplazamiento lateral con ligera rotación
            # Para orbitar en sentido horario manteniendo el frente al objeto:
            print("Orbitando...")
            # Combinación típica Mecanum para strafe circular:
            # FrontLeft: +, FrontRight: -, RearLeft: -, RearRight: +
            # Ajustamos valores para que "cierre" el círculo hacia el objeto
            robot.set_motor_model(800, -200, -200, 800) 
            
except KeyboardInterrupt:
    stop_robot()
    print("Detenido por el usuario")