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
        self.distance = 0 #variable que mide la distancia a la que están los obstaculos
        self.k = 1 #corrección de velocidad
        self.movement = 'stop' #variable que identifica cúal es el movimiento actual
        self.adc_readings = {'left_light': 0, 'right_light': 0, 'battery': 0}
        self.infrared_readings = {'center': 0, 'left': 0, 'right': 0}

        self._running = True
        self.buzzer_active = False
        self.enable_antichoque = False

        # El hilo que solo se encarga de ADC
        self.thread_adc = Thread(target=self.update_adc, daemon=True)
        self.thread_adc.start()

        # El hilo que solo se encarga de Infrarrojos
        self.thread_infrared = Thread(target=self.update_infrared, daemon=True)
        self.thread_infrared.start()
        
        # El hilo solo se encarga de actualizar la lectura del sensor de ultrasonidos
        self.thread = Thread(target=self.update_ultrasonic, daemon=True)
        self.thread.start()

        #El hilo del buzzer
        self.thread_buzzer = Thread(target=self._buzzer_loop, daemon=True)
        self.thread_buzzer.start()

        # El hilo solo se encarga de controlar antichoque
        self.thread_anti = Thread(target=self.antichoque, daemon=True)
        self.thread_anti.start()

    def update_ultrasonic(self):
        '''Actualiza la lectura del ultrasonidos a la varible distance'''
        while self._running:
            dist = self.ultrasonic.get_distance()
            if dist is not None:
                self.distance = dist
            time.sleep(0.01)

    def update_adc(self):
        '''Actualiza la lectura de los ADC'''
        while self._running:
            # Lectura y guardado de datos
            self.adc_readings['left_light'] = self.adc.read_adc(0)
            self.adc_readings['right_light'] = self.adc.read_adc(1)
            
            # Cálculo de batería según versión de PCB
            multiplier = 3 if self.adc.pcb_version == 1 else 2
            self.adc_readings['battery'] = self.adc.read_adc(2) * multiplier
            
            time.sleep(0.5) 

    def update_infrared(self):
        '''Actualiza la lectura de los infrarrojos'''
        while self._running:
            self.infrared_readings['center'] = self.infrared.read_one_infrared(2)
            self.infrared_readings['left'] = self.infrared.read_one_infrared(1)
            self.infrared_readings['right'] = self.infrared.read_one_infrared(3)
            time.sleep(0.05)

    #funciones del buzzer
    def _buzzer_loop(self):
        """Gestiona el parpadeo del sonido sin bloquear el robot."""
        while self._running:
            if self.buzzer_active:
                self.buzzer.set_state(True)
                time.sleep(0.5)
                self.buzzer.set_state(False)
                time.sleep(0.5)
            else:
                self.buzzer.set_state(False)
                time.sleep(0.1) # Pequeña pausa para no saturar la CPU

    def set_beeping(self, active: bool):
        """Método para encender/apagar el modo intermitente."""
        self.buzzer_active = active

    def beep_once(self, duration=0.1):
        """Pitido rápido único (útil para avisos cortos)."""
        self.buzzer.set_state(True)
        time.sleep(duration)
        self.buzzer.set_state(False)
            
    def set_servo(self, channel, angle, error=10):
        '''Método para mover los servo'''
        self.servo.set_servo_pwm(str(channel), angle, error)
    
    def forward(self, speed=600):
        # Avanza hacia delante
        self.movement = 'forward'
        self.v = speed
        self.PWM.set_motor_model(-speed, -speed, -speed, -speed)
        self.buzzer_active = False
    
    def backward(self, speed=600):
        # Avanza hacia atrás
        self.movement = 'backward'
        self.v = speed
        self.PWM.set_motor_model(speed, speed, speed, speed)
        self.buzzer_active = True
        
    def stop(self):
        # Parar el motor
        self.movement = 'stop'
        self.v = 0
        self.PWM.set_motor_model(0, 0, 0, 0)
        self.buzzer_active = False
        
    def turn_right(self, speed=600):
        # Giro a la derecha
        self.movement = 'turn_right'
        self.v = speed
        self.PWM.set_motor_model(-speed, -speed, 0, 0)
        self.buzzer_active = False
        
    def turn_left(self, speed=600):
        # Giro a la izquierda
        self.movement = 'turn_left'
        self.v = speed
        self.PWM.set_motor_model(0, 0, -speed, -speed)
        self.buzzer_active = False
        
    def clockwise_turn(self, speed=600):
        # Spin en sentido horario
        self.movement = 'clockwise_turn'
        self.v = speed
        self.PWM.set_motor_model(-speed, -speed, speed, speed)
        self.buzzer_active = False
    
    def counterclockwise_turn(self, speed=600):
        # Spin en sentido antihorario
        self.movement = 'counterclockwise_turn'
        self.v = speed
        self.PWM.set_motor_model(speed, speed, -speed, -speed)
        self.buzzer_active = False
    
    def right_lateral_movement(self, speed=600):
        # Movimiento lateral a la derecha
        self.movement = 'right_lateral'
        self.v = speed
        self.PWM.set_motor_model(-speed, speed, speed, -speed)
        self.buzzer_active = False
    
    def left_lateral_movement(self, speed=600):
        # Movimiento lateral a la izquierda
        self.movement = 'left_lateral'
        self.v = speed
        self.PWM.set_motor_model(speed, -speed, -speed, speed)
        self.buzzer_active = False
    
    def forward_left_diagonal_movement(self, speed=600):
        # Movimiento diagonal a la izquierda hacia adelante
        self.movement = 'forward_left_diagonal'
        self.v = speed
        self.PWM.set_motor_model(0, -speed, -speed, 0)
        self.buzzer_active = False
    
    def forward_right_diagonal_movement(self, speed=600):
        # Movimiento diagonal a la derecha hacia adelante
        self.movement = 'forward_right_diagonal'
        self.v = speed
        self.PWM.set_motor_model(-speed, 0, 0, -speed)
        self.buzzer_active = False
    
    def backward_left_diagonal_movement(self, speed=600):
        # Movimiento diagonal a la izquierda hacia atrás
        self.movement = 'backward_left_diagonal'
        self.v = speed
        self.PWM.set_motor_model(speed, 0, 0, speed)
        self.buzzer_active = True
    
    def backward_right_diagonal_movement(self, speed=600):
        # Movimiento diagonal a la derecha hacia atrás
        self.movement = 'backward_right_diagonal'
        self.v = speed
        self.PWM.set_motor_model(0, speed, speed, 0)
        self.buzzer_active = True

    def clockwise_orbit(self):
        # Orbita horaria
        self.movement = 'clockwise_orbit'
        self.v = 4000
        self.PWM.set_motor_model(1200, -4000, -800, 4000)
        self.buzzer_active = False # Generalmente las órbitas no activan buzzer
    
    def counter_clockwise_orbit(self):
        # Orbita antihoraria
        self.movement = 'counter_clockwise_orbit'
        self.v = 4000
        self.PWM.set_motor_model(-1200, 4000, 800, -4000)
        self.buzzer_active = False

    def free(self, speed1, speed2, speed3, speed4):
        # Movimiento libre con lógica de buzzer para retroceso
        self.movement = 'free'
        self.v = max(abs(speed1), abs(speed2), abs(speed3), abs(speed4))
        self.PWM.set_motor_model(speed1, speed2, speed3, speed4)
        
        # El buzzer se activa si los valores indican marcha atrás (positivos en este modelo)
        if speed1 > 0 and speed2 > 0 and speed3 > 0 and speed4 > 0:
            self.buzzer_active = True
        elif speed1 == 0 and speed2 > 0 and speed3 > 0 and speed4 == 0:
            self.buzzer_active = True
        elif speed1 > 0 and speed2 == 0 and speed3 == 0 and speed4 > 0:
            self.buzzer_active = True
        elif speed1 > 0 and speed2 > 0 and speed3 == 0 and speed4 == 0:
            self.buzzer_active = True
        elif speed1 == 0 and speed2 == 0 and speed3 > 0 and speed4 > 0:
            self.buzzer_active = True
        elif speed1 > 0 and speed2 == 0 and speed3 > 0 and speed4 == 0:
            self.buzzer_active = True
        elif speed1 == 0 and speed2 > 0 and speed3 == 0 and speed4 > 0:
            self.buzzer_active = True
        else:
            self.buzzer_active = False

    def antichoque(self):
        '''Lógica para antichoque: 
        en la proximidad reduce la velocidad en un factor 0,6 cuando está muy cerca detiene el robot. 
        No permite movimientos miestras detecte el obstáculo. 
        Hay que lanzar de nuevo el movimiento'''
        while True:
            if self.enable_antichoque:
                if self.distance < 30:
                    self.stop()
                elif 30 <= self.distance < 60:
                    self.k = 0.6
                    if self.movement == 'forward':
                        self.forward(int(self.v * self.k))
                    elif self.movement == 'backward':
                        self.backward(int(self.v * self.k))
                    elif self.movement == 'turn_left':
                        self.turn_left(int(self.v * self.k))
                    elif self.movement == 'turn_right':
                        self.turn_right(int(self.v * self.k))
                    elif self.movement == 'clockwise_turn':
                        self.clockwise_turn(int(self.v * self.k))
                    elif self.movement == 'counterclockwise_turn':
                        self.counterclockwise_turn(int(self.v * self.k))
                    elif self.movement == 'right_lateral':
                        self.right_lateral_movement(int(self.v * self.k))
                    elif self.movement == 'left_lateral':
                        self.left_lateral_movement(int(self.v * self.k))
                    elif self.movement == 'forward_left_diagonal':
                        self.forward_left_diagonal_movement(int(self.v * self.k))
                    elif self.movement == 'forward_right_diagonal':
                        self.forward_right_diagonal_movement(int(self.v * self.k))
                    elif self.movement == 'backward_left_diagonal':
                        self.backward_left_diagonal_movement(int(self.v * self.k))
                    elif self.movement == 'backward_right_diagonal':
                        self.backward_right_diagonal_movement(int(self.v * self.k))
                    elif self.movement == 'clockwise_orbit':
                        self.clockwise_orbit() 
                    elif self.movement == 'counter_clockwise_orbit':
                        self.counter_clockwise_orbit()
                    else:
                        self.stop()
                else:
                    self.k = 1

    def close(self):
        #Cerrar los motores
        self.stop()
        self.PWM.close()
        self.ultrasonic.close()
        self.infrared.close()
        self.buzzer.set_state(False)
        self.buzzer.close()