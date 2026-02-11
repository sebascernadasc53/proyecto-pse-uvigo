from motor import Ordinary_Car
from ultrasonic import Ultrasonic
from infrared import Infrared
from adc import ADC
from servo import Servo
from buzzer import Buzzer
import time
from threading import Thread

class Robot:
    def __init__(self):
        self.ultrasonic = Ultrasonic()
        self.PWM = Ordinary_Car()
        self.adc = ADC()
        self.servo = Servo()
        self.infrared = Infrared()
        self.buzzer = Buzzer()
        self.distance = 0
        self.adc_readings = {'left_light': 0, 'right_light': 0, 'battery': 0}
        self.infrared_readings = {'center': 0, 'left': 0, 'right': 0}

        self._running = True

        # El hilo que solo se encarga de ADC
        self.thread_adc = Thread(target=self.update_adc, daemon=True)
        self.thread_adc.start()

        # El hilo que solo se encarga de Infrarrojos
        self.thread_infrared = Thread(target=self.update_infrared, daemon=True)
        self.thread_infrared.start()
        
        # El hilo solo se encarga de actualizar la lectura del sensor de ultrasonidos
        self.thread = Thread(target=self.update_ultrasonic, daemon=True)
        self.thread.start()

    def update_ultrasonic(self):
        while self._running:
            dist = self.ultrasonic.get_distance()
            if dist is not None:
                self.distance = dist
            time.sleep(0.01)

    def update_adc(self):
        while self._running:
            # Lectura y guardado de datos
            self.adc_readings['left_light'] = self.adc.read_adc(0)
            self.adc_readings['right_light'] = self.adc.read_adc(1)
            
            # Cálculo de batería según versión de PCB
            multiplier = 3 if self.adc.pcb_version == 1 else 2
            self.adc_readings['battery'] = self.adc.read_adc(2) * multiplier
            
            time.sleep(0.5) 

    def update_infrared(self):
        while self._running:
            self.infrared_readings['center'] = self.infrared.read_one_infrared(2)
            self.infrared_readings['left'] = self.infrared.read_one_infrared(1)
            self.infrared_readings['right'] = self.infrared.read_one_infrared(3)
            time.sleep(0.05)
            
    def set_servo(self, channel, angle, error=10):
        self.servo.set_servo_pwm(str(channel), angle, error)
    
    def forward(self,speed=600):
        # Avanza hacia delante
        self.PWM.set_motor_model(-speed,-speed,-speed,-speed)
    
    def backward(self, speed=600):
        # Avanza hacia atrás
        self.PWM.set_motor_model(speed,speed,speed,speed)
        
    def stop(self):
        # Parar el moto
        self.PWM.set_motor_model(0,0,0,0)
        
    def turn_right(self,speed=600):
        #Giro a la derecha
        self.PWM.set_motor_model(-speed,-speed,0,0)
        
    def turn_left(self,speed=600):
        #Giro a la izquierda
        self.PWM.set_motor_model(0,0,-speed,-speed)
        
    def clockwise_turn(self,speed=600):
        #Spin en sentido horario
        self.PWM.set_motor_model(-speed,-speed,speed,speed)
    
    def counterclockwise_turn(self,speed=600):
        #Spin en sentido antihorario
        self.PWM.set_motor_model(speed,speed,-speed,-speed)
    
    def right_lateral_movement(self,speed=600):
        #Movimiento lateral a la derecha
        self.PWM.set_motor_model(-speed,speed,speed,-speed)
    
    def left_lateral_movement(self,speed=600):
        #Movimiento lateral a la izquierda
        self.PWM.set_motor_model(speed,-speed,-speed,speed)
    
    def forward_left_diagonal_movement(self,speed=600):
        #Movimiento diagonal a la izquierda hacia adelante
        self.PWM.set_motor_model(0,-speed,-speed,0)
    
    def forward_right_diagonal_movement(self,speed=600):
        #Movimiento diagonal a la derecha hacia adelante
        self.PWM.set_motor_model(-speed,0,0,-speed)
    
    def backward_left_diagonal_movement(self,speed=600):
        #Movimiento diagonal a la izquierda hacia atrás
        self.PWM.set_motor_model(0,speed,speed,0)
    
    def backward_right_diagonal_movement(self,speed=600):
        #Movimiento diagonal a la derecha hacia atrás
        self.PWM.set_motor_model(speed,0,0,speed)

    def clockwise_orbit(self):
        #orbita horaria
        self.PWM.set_motor_model(1200,-4000,-800,4000)
    
    def counter_clockwise_orbit(self):
        #orbita antihoraria
        self.PWM.set_motor_model(-1200,4000,800,-4000)
    
    def free(self,speed1,speed2,speed3,speed4):
        #Movimiento libre
        self.PWM.set_motor_model(speed1,speed2,speed3,speed4)
    
    def close(self):
        #Cerrar los motores
        self.stop()
        self.PWM.close()
        self.ultrasonic.close()
        self.infrared.close()
        self.adc.close()
        self.servo.close()