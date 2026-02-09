import time
#from motor import Ordinary_Car 
from threading import Thread
from robot import Robot
distance = 150
#ultrasonic = Ultrasonic()
#PWM = Ordinary_Car()
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

# VERIFICACION
def verificar_objeto():
    print("Analizando orbitabilidad...")
    robot.stop()
    lecturas = []
    for _ in range (5):
        robot.counter_clockwise_orbit()
        '''PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3])'''
        time.sleep(0.3)
        robot.stop()
        time.sleep(0.3)
        lecturas.append(distance)
        
    if len(lecturas) < 3:
        print(f"No hay suficientes lecturas, {(len(lecturas))},para verificar el objeto")
        return False
    elif max(lecturas) >=D_TARGET + TOL or min(lecturas) < D_TARGET - TOL:
        print("No orbitable")
        return False
    else:
        print("Orbitable")
        return True
#ORBITA
def orbitar_objeto():
    
    print("Orbitando")
    robot.counter_clockwise_orbit()
    #PWM.set_motor_model(Speed[0], Speed[1], Speed[2], Speed[3])
    if distance >=D_TARGET + 2*TOL or distance < D_TARGET - 2*TOL:
        print("Órbita perdida")
        robot.stop()
    time.sleep(0.1)
# MAIN
def main():
    global running
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
                robot.forward(300)

            elif distance < D_TARGET - 2*TOL:
                robot.backward(500)
                print("Demasiado cerca, retrocediendo")
            else:
                if verificar_objeto():
                    orbitar_objeto()
            time.sleep(0.05)
    except KeyboardInterrupt:
        running = False
        print("Abortando programa")
        robot.stop()
if __name__ == "__main__":
    main()
