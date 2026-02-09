import time
from motor import Ordinary_Car 
from threading import Thread
from robot import Robot

ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
D_TARGET = 50  # Distancia deseada al objeto (cm)
TOL = 10
Speed = [-1200,4000,800,-4000]
running = True
robot = Robot()
 # HILO SENSOR
def sensor_thread():
    global distance
    while running:
        lectura = robot.distance()
        if lectura is not None:
            distance = lectura
        time.sleep(0.05)
def verificar_objeto():
    print("Analizando orbitabilidad...")
    robot.stop
    lecturas = []
    for _ in range (10):
        Robot.counter_clockwise_orbit
        #PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3]) #orbita
        robot.stop
        time.sleep(0.3)
        lecturas.append(distance)
        time.sleep(0.3)
        
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
    for _ in (5):
        print("Orbitando")
        robot.counter_clockwise_orbit
        #PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3])
        if distance >=D_TARGET + 2*TOL or distance < D_TARGET - 2*TOL:
            print("Órbita perdida")
            Robot.stop
            break
        time.sleep(0.1)
def main():
    t = Thread(target=sensor_thread)
    t.daemon = True
    t.start()
    #bucle principal, buscar objeto
    try:
        while True:

            if distance > D_TARGET + 4*TOL:
                robot.forward(500)
                print("Buscando objetivo")

            elif distance > D_TARGET + 2*TOL:
                PWM.set_motor_model(-300,-300,-300,-300)

            elif distance < D_TARGET - 2*TOL:
                PWM.set_motor_model(500,500,500,500)
                print("Demasiado cerca, retrocediendo")
            else:
                if verificar_objeto():
                    orbitar_objeto()
    except KeyboardInterrupt:
        running = False
        print("Abortando programa")
        robot.stop
if __name__ == "__main__":
    main()
