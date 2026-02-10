from motor import Ordinary_Car
from infrared import Infrared
import time

# --- CONFIGURACIÓN ---
# Usamos constantes para que sea fácil ajustar la velocidad sin buscar en el código
VEL_AVANCE = 800      # Velocidad suave para ir recto
VEL_GIRO_S = 800     # Giro suave
VEL_GIRO_F = 800     # Giro fuerte (para curvas cerradas)
PAUSA_CICLO = 0.001    # 50ms (equilibrio entre rapidez y estabilidad)

# --- INICIALIZACIÓN ---
car = Ordinary_Car()
sensores = Infrared()

print("--- Sistema de Seguimiento de Línea Activo ---")
print("Presiona Ctrl+C en VS Code para detener el coche.")

# --- Antes del bucle while ---
ultima_direccion = "centro" 

try:
    while True:
        estado = sensores.read_all_infrared()
        
        if estado == 2: # Centro
            car.set_motor_model(-VEL_AVANCE, -VEL_AVANCE, -VEL_AVANCE, -VEL_AVANCE)
            ultima_direccion = "centro"
            
        elif estado in [4, 6]: # Izquierda
            car.set_motor_model(VEL_GIRO_S, VEL_GIRO_S, -VEL_GIRO_S, -VEL_GIRO_S)
            ultima_direccion = "izquierda"
            
        elif estado in [1, 3]: # Derecha
            car.set_motor_model(-VEL_GIRO_S, -VEL_GIRO_S, VEL_GIRO_S, VEL_GIRO_S)
            ultima_direccion = "derecha"
            
        elif estado == 0: 
            # En lugar de sleeps, usamos la memoria
            print("Buscando línea...")
            if ultima_direccion == "izquierda":
                # Si se perdió por la izquierda, gira sobre su eje a la izquierda para buscar
                car.set_motor_model(VEL_GIRO_S, VEL_GIRO_S, -VEL_GIRO_S, -VEL_GIRO_S)
            elif ultima_direccion == "derecha":
                car.set_motor_model(-VEL_GIRO_S, -VEL_GIRO_S, VEL_GIRO_S, VEL_GIRO_S)
            else:
                # Si no sabe dónde está, retrocede lento
                car.set_motor_model(400, 400, 400, 400)

        time.sleep(PAUSA_CICLO) # Esta es la única pausa que debe existir

except KeyboardInterrupt:
    # Si pulsas el botón de Stop en VS Code o Ctrl+C
    print("\n[!] Detención manual detectada.")

finally:
    # Esto se ejecuta SIEMPRE al final para evitar que el coche siga moviéndose solo
    car.set_motor_model(0, 0, 0, 0)
    sensores.close() # Liberamos los sensores (como en tu código de infrared.py)
    print("--- Programa finalizado de forma segura ---")