import time
from threading import Thread, Lock
from ultrasonic import Ultrasonic
from servo import Servo
from moves import Moves

# VARIABLES GLOBALES
distance_front = 150 
current_angle = 70
running = True
data_lock = Lock() # Evitar conflictos entre hilos

# Movimiento cabeza radar
def hilo_radar(sensor, cuello):
    global distance_front, current_angle, running
    
    ANGULO_CENTRO = 70
    ANGULO_IZQ = 20
    ANGULO_DER = 120
    
    # Barrido: 20 -> 120 -> 20
    recorrido = list(range(ANGULO_IZQ, ANGULO_DER + 1, 10)) + list(range(ANGULO_DER, ANGULO_IZQ - 1, -10))

    while running:
        for angulo in recorrido:
            if not running: break
            
            cuello.set_servo_pwm('0', angulo)
            time.sleep(0.08)
            
            lectura = sensor.get_distance()
            if lectura is not None:
                with data_lock:
                    distance_front = lectura
                    current_angle = angulo

# Lógica
def hilo_motores(robot):
    global distance_front, current_angle, running
    print("[Sistema] Lógica de movimiento activa")

    while running:
        with data_lock:
            dist = distance_front
            ang = current_angle

        es_frente = (60 <= ang <= 80)
        
        if dist < 25 and es_frente:
            # OBSTÁCULO DETECTADO
            print(f"[!] Objeto a {dist}cm. Buscando salida...")
            robot.stop()
            
            # Iniciamos giro sobre sí mismo
            robot.clockwise_turn(800)
            
            # Bucle de espera ACTIVA: No sale de aquí hasta que vea camino libre al frente
            buscando = True
            while buscando and running:
                with data_lock:
                    d_scan = distance_front
                    a_scan = current_angle
                
                # Condición para parar el giro: 
                # Camino despejado (>80cm) Y la cabeza está pasando por el centro (70)
                if d_scan > 80 and (65 <= a_scan <= 75):
                    print(f"[OK] Salida encontrada ({d_scan}cm).")
                    robot.stop()
                    buscando = False
                
                time.sleep(0.05)
        
        else:
            # CAMINO LIBRE
            robot.forward(900)
            
        time.sleep(0.1)

# ===== FUNCIÓN PRINCIPAL =====
def main():
    global running

    ultrasonic = Ultrasonic()
    servo = Servo()
    robot = Moves()

    # Centrar al inicio
    servo.set_servo_pwm('0', 70)
    time.sleep(1)

    # Creación de hilos con la estructura solicitada
    t_radar = Thread(target=hilo_radar, args=(ultrasonic, servo), daemon=True)
    t_robot = Thread(target=hilo_motores, args=(robot,), daemon=True)

    try:
        t_radar.start()
        t_robot.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[CTRL+C] Deteniendo...")
        running = False
        time.sleep(0.5)
    finally:
        robot.stop()
        print("[OK] Robot apagado")

if __name__ == "__main__":
    main()