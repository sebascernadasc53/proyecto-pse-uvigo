# proyecto-pse-uvigo
Repositorio relativo al proyecto de la asignatura de Programación de sistemas embebidos del Máster en Mecatrónica de la UVIGO Curso 2025/2026

# Autores del proyecto
Adrián Carrera Martínez,
Sebastián Carlos Cernadas Cernadas,
Martín Ferreira Pérez,
Iker Moo Barros.

# Robot utilizado 
Freenove 4WD Mecanum Wheels:

https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi

# Instrucciones
1. Descargar https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi en el robot
2. Descargar este repositorio
3. Tienen que estar en la misma carpeta los archivos de este repositorio con los de que hay en Code/Server del repositorio de Freenove
4. Ya está listo para ejecutarse los programas

# Descripción Programas
1. Siguelineas.py : Como su nombre indica, al ejecutar el código el robot empieza a seguir la línea
2. antichoque.py : Al ejecutarse, el robot avanza hacia delante hasta que detecta un obstáculo y frena
3. Programa de aviso a la oscuridad.py : Activa la bocina cuando las resistencias sensibles a la luz detectan que el entorno está oscuro
4. roombaadri.py : Este programa mueve el robot evitando chocarse con las paredes al estilo de un robot aspirador tipo roomba
5. app.py : Interfaz de control del robot. Permite mover el robot, la posición de los ultrasonidos y obtener las lecturas de los sensores
6. robot.py : define la clase Robot

# Clase Robot
En robot.py está definida la clase Robot
Están definidos los métodos con diferentes posibles movimientos:
1. forward
2. backward
3. stop        
4. turn_right
5. counterclockwise_turn
6. right_lateral_movement   
7. left_lateral_movement
8. forward_left_diagonal_movement
9. forward_right_diagonal_movement
10. backward_left_diagonal_movement
11. backward_right_diagonal_movement
12. clockwise_orbit   
13. counter_clockwise_orbit
14. free

Están definidos los métodos para la lectura de sensores
1. update_ultrasonic
2. update_adc
3. update_infrared


