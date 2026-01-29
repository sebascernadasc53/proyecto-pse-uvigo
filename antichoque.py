from motor import Ordinary_Car
from ultrasonic import Ultrasonic
import time

ultrasonic = Ultrasonic()
PWM = Ordinary_Car() 

try:
    print("Inicio ...")
    while True:
        distance = ultrasonic.get_distance()  # obtener distancia ultrasonidos
        if distance is not None:
            print(f"Distancia ultrasonidos: {distance} cm")  # Print distancia
        time.sleep(0.5)  # espera

        if distance > 10:
            PWM.set_motor_model(100,100,100,100) #Avance
            print ("El robot se está moviendo")
        else:
            PWM.set_motor_model(0,0,0,0) #Stop
            print ("El robot está parado")

        

except KeyboardInterrupt:  # Cierre (Ctrl+C)
    ultrasonic.close()
    PWM.close() # Cerrar PWM 
finally:
    print("\nEnd of program")  # Print cierre
