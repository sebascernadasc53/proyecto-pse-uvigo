from motor import Ordinary_Car
from infrared import Infrared
import time

# --- CONFIGURACIÓN ---
# Usamos constantes para que sea fácil ajustar la velocidad sin buscar en el código
VEL_AVANCE = 800      # Velocidad suave para ir recto
VEL_GIRO_S = 2500     # Giro suave
VEL_GIRO_F = 4000     # Giro fuerte (para curvas cerradas)
PAUSA_CICLO = 0.05    # 50ms (equilibrio entre rapidez y estabilidad)

# --- INICIALIZACIÓN ---
car = Ordinary_Car()
sensores = Infrared()

print("--- Sistema de Seguimiento de Línea Activo ---")
print("Presiona Ctrl+C en VS Code para detener el coche.")

try:
    while True:
        # 1. Capturamos la lectura (el número "mágico" del 1 al 7)
        estado = sensores.read_all_infrared()
        
        # 2. Decidimos el movimiento basado en el número obtenido
        if estado == 2:
            # Línea al centro
            print(f"[{estado}] Recto")
            car.set_motor_model(VEL_AVANCE, VEL_AVANCE, VEL_AVANCE, VEL_AVANCE)
            
        elif estado == 4:
            # Solo izquierda detecta: corregir girando a la izquierda
            print(f"[{estado}] Giro Suave Izquierda")
            car.set_motor_model(-1500, -1500, VEL_GIRO_S, VEL_GIRO_S)
            
        elif estado == 6:
            # Izquierda y Centro detectan: giro más agresivo
            print(f"[{estado}] Giro FUERTE Izquierda")
            car.set_motor_model(-2000, -2000, VEL_GIRO_F, VEL_GIRO_F)
            
        elif estado == 1:
            # Solo derecha detecta: corregir girando a la derecha
            print(f"[{estado}] Giro Suave Derecha")
            car.set_motor_model(VEL_GIRO_S, VEL_GIRO_S, -1500, -1500)
            
        elif estado == 3:
            # Derecha y Centro detectan: giro más agresivo
            print(f"[{estado}] Giro FUERTE Derecha")
            car.set_motor_model(VEL_GIRO_F, VEL_GIRO_F, -2000, -2000)
            
        else:
            # Valor 7 (todo negro) o 0 (todo blanco): Paramos por seguridad
            print(f"[{estado}] Fuera de línea / Parada")
            car.set_motor_model(0, 0, 0, 0)

        # 3. Espera mínima para que el procesador respire
        time.sleep(PAUSA_CICLO)

except KeyboardInterrupt:
    # Si pulsas el botón de Stop en VS Code o Ctrl+C
    print("\n[!] Detención manual detectada.")

finally:
    # Esto se ejecuta SIEMPRE al final para evitar que el coche siga moviéndose solo
    car.set_motor_model(0, 0, 0, 0)
    sensores.close() # Liberamos los sensores (como en tu código de infrared.py)
    print("--- Programa finalizado de forma segura ---")