from motor import Ordinary_Car

class Moves:
    def __init__(self):
        self.PWM = Ordinary_Car() #Inicializa los motores
        
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
    
    def free(self,speed1,speed2,speed3,speed4):
        #Movimiento libre
        self.PWM.set_motor_model(speed1,speed2,speed3,speed4)
    
    def close(self):
        #Cerrar los motores
        self.PWM.close()
        