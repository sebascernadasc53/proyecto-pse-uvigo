import time
from threading import Thread
from ultrasonic import Ultrasonic
from servo import Servo
from moves import Moves

# Variables globales
# distance[0]=Izq, distance[1]=Centro, distance[2]=Der
distances = [100, 100, 100] 
running = True

def hilo_radar(sensor, cuello):
    global distances, running
    print("[Sistema] Radar horizontal iniciado (Escaneo de 3 puntos)")

    # Definimos los 3 ángulos clave de visión
    ANGULOS = {'IZQ': 110, 'CENTRO': 70, 'DER': 30}
    
    while running:
        # Escaneo hacia la izquierda
        cuello.set_servo_pwm('0', ANGULOS['IZQ'])
        time.sleep(0.2)
        distances[0] = sensor.get_distance()

        # Escaneo al centro
        cuello.set_servo_pwm('0', ANGULOS['CENTRO'])
        time.sleep(0.2)
        distances[1] = sensor.get_distance()

        # Escaneo a la derecha
        cuello.set_servo_pwm('0', ANGULOS['DER'])
        time.sleep(0.2)
        distances[2] = sensor.get_distance()

def hilo_motores(robot):
    global distances, running
    print("[Sistema] Lógica de evasión activa")

    while running:
        izq, centro, der = distances

        # 1. EMERGENCIA: Obstáculo al frente
        if centro < 35:
            print(f"[!] Obstáculo frontal: {centro}cm")
            robot.backward(1000) # Retrocede
            time.sleep(0.3)
            
            # Decide hacia dónde girar según el espacio lateral
            if izq > der:
                robot.counter_clockwise_turn(1200) # Gira a la izquierda
            else:
                robot.clockwise_turn(1200) # Gira a la derecha
            time.sleep(0.5)

        # 2. PRECAUCIÓN: Algo cerca por la izquierda
        elif izq < 25:
            print(" -> Corrigiendo hacia la derecha")
            robot.clockwise_turn(800) 
            time.sleep(0.2)

        # 3. PRECAUCIÓN: Algo cerca por la derecha
        elif der < 25:
            print(" <- Corrigiendo hacia la izquierda")
            robot.counter_clockwise_turn(800)
            time.sleep(0.2)

        # 4. CAMINO LIBRE
        else:
            robot.forward(900)

        time.sleep(0.05)

def main():
    global running
    ultrasonic = Ultrasonic()
    servo = Servo()
    robot = Moves()

    print("[Config] Centrando sensor...")
    servo.set_servo_pwm('0', 70)
    time.sleep(1)

    # Creamos los hilos para que corran en paralelo
    t_radar = Thread(target=hilo_radar, args=(ultrasonic, servo), daemon=True)
    t_robot = Thread(target=hilo_motores, args=(robot,), daemon=True)

    try:
        t_radar.start()
        t_robot.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Terminando]...")
        running = False
    finally:
        running = False
        robot.stop()
        print("[OK] Sistema apagado")

if __name__ == "__main__":
    main()