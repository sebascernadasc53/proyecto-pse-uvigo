from motor_sim import Ordinary_Car
from ultrasonic_sim import Ultrasonic
import time
from threading import Thread

class Robot:
    def __init__(self):
        self.ultrasonic = Ultrasonic()
        self.PWM = Ordinary_Car()
        self.distance = 0
        self._running = True
        
        # El hilo solo se encarga de actualizar la lectura del sensor de ultrasonidos
        self.thread = Thread(target=self.update_ultrasonic, daemon=True)
        self.thread.start()

    def update_ultrasonic(self):
        while self._running:
            dist = self.ultrasonic.get_distance()
            if dist is not None:
                self.distance = dist
            time.sleep(0.05)
    
    def motores(self,v):
        self.PWM.set_motor_model(v, v, v, v)
        
    def detener(self):
        self.PWM.set_motor_model(0, 0, 0, 0)

    def finalizar(self):
        self._running = False
        self.detener()