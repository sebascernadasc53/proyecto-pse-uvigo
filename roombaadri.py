import time
from threading import Thread
from ultrasonic import Ultrasonic
from servo import Servo
from moves import Moves

# Variables
distance = 70 # Distancia en cm a la que robot detecta
running = True


def hilo_radar(sensor, cuello):
    global distance
    print("[Sistema] Radar Pan-Tilt (2 servos) iniciado...")
    
    # Angulo para el servo '1' (Tilt - Vertical)
    ANGULO_TILT_FIJO = 70
    
    while running:
        # Mantenemos el servo de inclinación firme para que no se caiga la cabeza
        cuello.set_servo_pwm('1', ANGULO_TILT_FIJO)

        # Barrido HORIZONTAL (Servo '0' - Pan)
        recorrido = list(range(45, 136, 10)) + list(range(135, 44, -10))
        
        for angulo in recorrido:
            if not running: break
            
            # Movimiento del cuello
            cuello.set_servo_pwm('0', angulo)
            
            # Tiempo de asentamiento mecánico (crucial para evitar vibración)
            time.sleep(0.08)
            
            # Actualización de la distancia
            lectura = sensor.get_distance()
            if lectura is not None:
                distance = lectura

# LÓGICA DE LA ROOMBA
def hilo_motores(robot):
    global distance
    print("[Sistema] Lógica Roomba activa...")
    
    while running:
        # 1. ESTADO: CAMINO LIBRE (Avance rápido)
        if distance > 60:
            robot.forward(1000)
            

        # 2. ESTADO: PRECAUCIÓN (Reducción de velocidad)
        elif 30 < distance <= 60:
            robot.forward(700)
            

        # 3. ESTADO: EVASIÓN (Giro a la derecha)
        else:
            print(f"[!] Obstáculo a {distance}cm. Maniobrando...")
            robot.stop()
            time.sleep(0.2)
            
            # Retroceder un poco para facilitar el giro mecánico
            robot.backward(1000)
            time.sleep(0.5)
            
            # Giro típico de Roomba (Siempre derecha sobre su eje)
            robot.clockwise_turn(1200)
            time.sleep(0.8) # Hay que ajustar este tiempo para controlar el ángulo de giro, depende de la velocidad
            robot.stop()
            time.sleep(0.1)


def main():
    global running
    
    # Inicialización de hardware a través de tus clases
    u = Ultrasonic()
    s = Servo()
    m = Moves()

    # Reset de servos a posición neutral
    print("[Config] Calibrando servos...")
    s.set_servo_pwm('0', 90)
    s.set_servo_pwm('1', 90)
    time.sleep(1)

    # Definición y lanzamiento de hilos
    t_radar = Thread(target=hilo_radar, args=(u, s), daemon=True)
    t_robot = Thread(target=hilo_motores, args=(m,), daemon=True)

    try:
        t_radar.start()
        t_robot.start()
        
        # El programa principal se queda aquí esperando
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[Terminar] Deteniendo procesos...")
        running = False
        time.sleep(0.5)
        
    finally:
        running = False
        m.stop()
        m.close()
        u.close()
        print("[OK] Robot detenido y puertos cerrados.")

if __name__ == "__main__":
    main()