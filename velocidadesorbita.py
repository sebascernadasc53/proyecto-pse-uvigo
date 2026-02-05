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
          print("Peso Traslación = Peso Rotación")
          PWM.set_motor_model(0,2000,0,-2000)
          print("0,2000,0,-2000")
          time.sleep(2)

          #ROTACIÓN
          print("Más peso a rotación, orbita más cerrada")
          PWM.set_motor_model(1000,2000,-1000,-2000)
          print("1000,2000,-1000,-2000")
          time.sleep(2)
          print("Otros valores")
          PWM.set_motor_model(1000,3000,-1000,-3000)
          print("1000,3000,-1000,-3000")
          time.sleep(2)
          print("Otros valores 2")
          PWM.set_motor_model(2000,4000,-2000,-4000)
          print("2000,4000,-2000,-4000")
          time.sleep(2)
          PWM.set_motor_model(0,0,0,0)
          print("COCHE PARADO, APROVECHA PARA RECOLOCARLO SI HAY POCO ESPACIO, 10 SECS")
          time.sleep(10)

          #TRANSLACIÓN
          print("Mayor peso en translación,órbitas más abiertas")
          PWM.set_motor_model(-1000,2000,-1000,2000)
          print("0,2000,0,-2000")
          time.sleep(2)
          print("Otros valores")
          PWM.set_motor_model(-1000,2000,1000,-2000)
          print("-1000,2000,1000,-2000")
          time.sleep(2)
          print("Otros valores 2")
          PWM.set_motor_model(-2000,1000,1000,-3000)
          print("-2000,1000,1000,-3000")
          time.sleep(2)

          
          
          



except KeyboardInterrupt:
    PWM.set_motor_model(0,0,0,0)
    print("Deteniendo calibración")
            
          
