import time
from threading import Thread
from robot import Robot 

# variables 
running = True
look_center = False

# Movimiento continuo de la cabeza del robot en horizontal
def hilo_radar(robot):
    global running, look_center
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
                robot.set_servo(0,70)  # Servo horizontal
            else:
                robot.set_servo(0,angulo)

            time.sleep(0.02)

# Lógica Roomba
def hilo_motores(robot):
    global running, look_center
    print("[Sistema] Lógica Roomba activa")

    while running:
        
        distancia_actual = robot.distance

        # CAMINO LIBRE
        if distancia_actual > 60:
            robot.forward(700)
            look_center = False # Radar modo barrido
            
        # PRECAUCIÓN
        elif 40 < distancia_actual <= 60:
            robot.forward(500)
            look_center = False # Radar modo barrido
        # OBSTÁCULO CERCA → MANIOBRA
        else:
            print(f"[!] Obstáculo a {distancia_actual} cm")
            
            # Paso 1: Parar el robot indmediatamente
            robot.stop()
            look_center = True
            time.sleep(0.1)
            
            #robot.backward(900)
            #time.sleep(0.3)
            
            # Paso 2: Girar hasta que el camino esté despejado (bucle que termina cuando la distancia es mayor que 40 cm)
            while robot.distance <= 45 and running:
                robot.clockwise_turn(800) # Gira sobre sí mismo en sentido horario
                time.sleep(0.05)
            
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
    robot.set_servo(0, 70)
    robot.set_servo(1, 90)
    time.sleep(1)

    # Hilos
    t_radar = Thread(target=hilo_radar, args=(robot,), daemon=True)
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
        robot._running  = False
        robot.stop()
        robot.close()
        print("[OK] Robot detenido correctamente")

if __name__ == "__main__":
    main()
    