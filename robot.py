from motor import Ordinary_Car
from ultrasonic import Ultrasonic
from infrared import Infrared
from adc import ADC
import time
from threading import Thread

class Robot:
    def __init__(self):
        self.ultrasonic = Ultrasonic()
        self.PWM = Ordinary_Car()
        self.adc = ADC()
        self.infrared = Infrared()

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
    
    def read_Adc(self):
        '''Lectura de los sensores ADC'''
        adc = ADC()
        try:
            print ("Leyendo ADC ...")
            while True:
                #fotoresistencia izquierda
                Left = adc.read_adc(0)
                print (f"Fotoresistencia izq: V = {Left} V")
                #fotoresistencia derecha
                Right = adc.read_adc(1)
                print (f"Fotoresistencia dcha: V = {Right} V")
                #batería
                Battery = adc.read_adc(2) * (3 if adc.pcb_version == 1 else 2)
                print (f"Batería: V = {Battery} V")
                #lectura cada 1 s
                print ('================================================')
                time.sleep(1)
        except KeyboardInterrupt:
            print ("\nEnd of program")

def read_Infrared(self):
    '''Lectura de los  infrarrojos'''
    infrared = Infrared()
    try:
        while True:
            #LECTURAS
            IR_centro = infrared.read_one_infrared(1)
            IR_izquierda = infrared.read_one_infrared(2)
            IR_derecha = infrared.read_one_infrared(3)
            #MOSTRAR LECTURAS
            if IR_centro != 1 and IR_izquierda == 1 and IR_derecha != 1:
                print ('Infrarrojos CENTRO')
            elif IR_centro != 1 and IR_izquierda != 1 and IR_derecha == 1:
                print ('Infrarrojos DERECHA')
            elif IR_centro == 1 and IR_izquierda != 1 and IR_derecha != 1:
                print ('Infrarrojos IZQUIERDA')
            print("========================================")
    except KeyboardInterrupt:
        infrared.close()
        print("\nEnd of program")
    
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
        self.PWM.set_motor_model(400,-4000,-400,4000)
    
    def counter_clockwise_orbit(self):
        #orbita antihoraria
        self.PWM.set_motor_model(-400,4000,400,-4000)
    
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