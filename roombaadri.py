import time
from threading import Thread
from ultrasonic import Ultrasonic
from servo import Servo
from moves import Moves

# variables 
distance = 150  # distancia medida por ultrasonidos (cm), este solo es un valor inicial luego ya toma el valor del ultrasonido
running = True

# Movimiento continuo de la cabeza del robot en horizontal
def hilo_radar(sensor, cuello):
    global distance, running
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

            cuello.set_servo_pwm('0', angulo)  # SOLO servo horizontal
            time.sleep(0.08)  

            lectura = sensor.get_distance()
            if lectura is not None:
                distance = lectura

# Lógica Roomba
def hilo_motores(robot):
    global distance, running
    print("[Sistema] Lógica Roomba activa")

    while running:

        # CAMINO LIBRE
        if distance > 80:
            robot.forward(1000)

        # PRECAUCIÓN
        elif 25 < distance <= 60:
            robot.forward(700)

        # OBSTÁCULO CERCA → MANIOBRA
        else:
            print(f"[!] Obstáculo a {distance} cm")

            robot.backward(900)
            time.sleep(0.4)

            robot.clockwise_turn(1200)
            time.sleep(0.5)

        time.sleep(0.05)

def main():
    global running

    # Inicialización de hardware
    ultrasonic = Ultrasonic()
    servo = Servo()
    robot = Moves()

    print("[Config] Centrando servo horizontal...")
    servo.set_servo_pwm('0', 70)
    time.sleep(1)

    # Hilos
    t_radar = Thread(target=hilo_radar, args=(ultrasonic, servo), daemon=True)
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
        ultrasonic.close()
        print("[OK] Robot detenido correctamente")

if __name__ == "__main__":
    main()
