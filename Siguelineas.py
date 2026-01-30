import time
from motor import Ordinary_Car
from infrared import Infrared

def run_follower():
    car = Ordinary_Car()
    sensors = Infrared()
    
    V = 1300  # Velocidad crucero
    T = 1500  # Velocidad de giro
    
    # Mapeo de estados: { estado_sensor: (rueda_1, rueda_2, rueda_3, rueda_4) }
    # 1: DI, 2: TI, 3: DD, 4: TD (según el orden de tu set_motor_model)
    TABLA_MOVIMIENTOS = {
        2: (V, V, V, V),       # [010] Centrado -> Recto
        4: (-T, -T, T, T),     # [100] Línea a la izq -> Girar Izquierda
        6: (-T, -T, T, T),     # [110] Línea a la izq -> Girar Izquierda
        1: (T, T, -T, -T),     # [001] Línea a la der -> Girar Derecha
        3: (T, T, -T, -T),     # [011] Línea a la der -> Girar Derecha
        7: (V, V, V, V),       # [111] Intersección -> Recto
        0: (0, 0, 0, 0)        # [000] Perdido -> Parar
    }

    print("Siguelíneas activo (Modo Diccionario).")

    try:
        while True:
            estado = sensors.read_all_infrared()
            
            # Buscamos el movimiento en el diccionario. 
            # Si el estado no existe, por defecto se detiene (0,0,0,0)
            motores = TABLA_MOVIMIENTOS.get(estado, (0, 0, 0, 0))
            
            # Aplicamos las velocidades usando "unpacking" de la tupla (*)
            car.set_motor_model(*motores)
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
    finally:
        car.close()
        sensors.close()

if __name__ == '__main__':
    run_follower()