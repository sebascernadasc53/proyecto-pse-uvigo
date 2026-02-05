# Pruebo distintos valores de translación + rotación para ver como reacciona el robot

import time
from motor import Ordinary_Car 
from ultrasonic import Ultrasonic
ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
dist = ultrasonic.get_distance()
PWM.set_motor_model(0,0,0,0)
try:
     while dist > 5:
          print("Probando órbitas horarias, para antihorarias cambiar signo")
          print(f"Distancia: {dist} cm")
          print("Peso Traslación = Peso Rotación") #esta funciona  pero las ruedas patinan un poco
          PWM.set_motor_model(0,4000,0,-4000)
          #TRANSLACIÓN
          print("Peso translación 1,5")
          PWM.set_motor_model(-500,2500,2000,-4000)
          print("-500,2500,2000,-4000")
          time.sleep(5)
          PWM.set_motor_model(0,0,0,0)
          time.sleep(2)         
          print("Peso translación 1,2")
          PWM.set_motor_model(-200,2200,1400,-3400)
          print("-200,2200,1400,-3400")
          time.sleep(5)
          PWM.set_motor_model(0,0,0,0)
          time.sleep(5)

          
          
          



except KeyboardInterrupt:
    PWM.set_motor_model(0,0,0,0)
    print("Deteniendo calibración")
            
          
