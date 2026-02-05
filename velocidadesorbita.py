# Pruebo distintos valores de translación + rotación para ver como reacciona el robot

import time
from motor import Ordinary_Car 
from ultrasonic import Ultrasonic
ultrasonic = Ultrasonic()
PWM = Ordinary_Car()
dist = ultrasonic.get_distance()
try:
     while dist < 50:
          print("Probando órbitas horarias, para antihorarias cambiar")
          print(f"Distancia: {dist} cm")
          print("Probando órbita horaria. Peso Traslación = Peso Rotación")
          PWM.set_motor_model(0,2000,0,-2000)
          print("0,2000,0,-2000")
          time.sleep(2)
          print(f"Distancia: {dist} cm")
          print("Más peso a rotación, orbita más cerrada")
          PWM.set_motor_model(1000,2000,-1000,-2000)
          print("1000,2000,-1000,-2000")
          time.sleep(2)
          print("Otros valores")
          PWM.set_motor_model(1000,3000,-1000,-3000)
          print("1000,3000,-1000,-3000")
          time.sleep(2)
          
