import time
from threading import Thread
from robot import Robot 

# variables 
distance = 150  # distancia medida por ultrasonidos (cm), este solo es un valor inicial luego ya toma el valor del ultrasonido
running = True
look_center = False

# Movimiento continuo de la cabeza del robot en horizontal
def hilo_radar(sensor, cuello):
    global distance, running, look_center
    print("[Sistema] Radar horizontal iniciado (1 servo)")

    ANGULO_CENTRO = 70
    ANGULO_IZQ = ANGULO_CENTRO - 30   # 40°
    ANGULO_DER = ANGULO_CENTRO + 30   # 100°

    # Barrido continuo izquierda → derecha → izquierda
    recorrido = (
        list(range(ANGULO_IZQ, ANGULO_DER + 1, 5)) +
        list(range(ANGULO_DER, ANGULO_IZQ - 1, -5))
    )

    while running:
        for angulo in recorrido:
            if not running:
                break
            if look_center:
                cuello.set_servo_pwm('0',70)  # Servo horizontal
            else:
                cuello.set_servo_pwm('0',angulo)

            time.sleep(0.02)
            lectura = sensor.get_distance()
            if lectura is not None:
                distance = lectura

# Lógica Roomba
def hilo_motores(robot):
    global distance, running, look_center
    print("[Sistema] Lógica Roomba activa")

    while running:

        # CAMINO LIBRE
        if distance > 60:
            robot.forward(700)
            look_center = False # Radar modo barrido
            
        # PRECAUCIÓN
        elif 30 < distance <= 60:
            robot.forward(500)
            look_center = False # Radar modo barrido
        # OBSTÁCULO CERCA → MANIOBRA
        else:
            print(f"[!] Obstáculo a {distance} cm")
            
            # Paso 1: Parar el robot indmediatamente
            robot.stop()
            look_center = True
            time.sleep(0.1)
            
            #robot.backward(900)
            #time.sleep(0.3)
            
            # Paso 2: Girar hasta que el camino esté despejado (bucle que termina cuando la distancia es mayor que 40 cm)
            while distance <= 45 and running:
                robot.clockwise_turn(800) # Gira sobre sí mismo en sentido horario
                time.sleep(0.1)
            print("[OK] Camino despejado, reanudando marcha.")
            time.sleep(0.05)
            robot.stop()
            time.sleep(0.1)

        time.sleep(0.05)

def main():
    global running

    # Inicialización de hardware
    robot = Robot()

    print("[Config] Centrando servo horizontal...")
    robot.set_servo_pwm('0', 70)
    robot.set_servo_pwm('1', 90)
    time.sleep(1)

    # Hilos
    t_radar = Thread(target=hilo_radar, args=(robot, robot), daemon=True)
    t_robot = Thread(target=hilo_motores, args=(robot,), daemon=True)

    try:
        t_radar.start()
        t_robot.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[CTRL+C] Deteniendo robot...")
        running = False
        time.sleep(0.3)

    finally:
        running = False
        robot.stop()
        robot.close()
        print("[OK] Robot detenido correctamente")

if __name__ == "__main__":
    main()
    