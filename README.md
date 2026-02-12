# proyecto-pse-uvigo
Repositorio relativo al proyecto de la asignatura de Programación de sistemas embebidos del Máster en Mecatrónica de la UVIGO Curso 2025/2026

# Autores del proyecto
- Adrián Carrera Martínez,
- Sebastián Carlos Cernadas Cernadas,
- Martín Ferreira Pérez,
- Iker Moo Barros.

# 🤖 Control de Robot Freenove 4WD (Mecanum Wheels)

Este repositorio contiene los scripts de control y la lógica de navegación para el **Freenove 4WD Smart Car Kit**, diseñado para Raspberry Pi y equipado con ruedas omnidireccionales Mecanum.

* **Hardware Base:** [Repositorio Oficial Freenove](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi)

---

## 🛠 Instalación y Configuración

Para asegurar el correcto funcionamiento, sigue estos pasos:

1.  **Clonar el repositorio oficial:** Descarga el código base de Freenove en tu Raspberry Pi.
2.  **Preparar este repositorio:** Descarga estos archivos y colócalos dentro de la carpeta `Code/Server` del repositorio original de Freenove.
    * *Nota: Esto es indispensable para que el script pueda importar las librerías de control de motores y sensores del fabricante.*
3.  **Listo para usar:** Una vez ubicados en la carpeta correcta, puedes ejecutar cualquier programa directamente.

---

## 📂 Descripción de Programas

| Archivo | Descripción |
| :--- | :--- |
| **`app.py`** | **Interfaz de Control:** Panel gráfico para mover el robot, controlar el servo del ultrasonido y ver lecturas en tiempo real. |
| **`robot.py`** | **Clase Core:** Define la clase `Robot` y toda la lógica de bajo nivel. |
| **`Siguelineas.py`** | El robot utiliza sus sensores infrarrojos para seguir una línea negra en el suelo. |
| **`antichoque.py`** | Avanza en línea recta y se detiene automáticamente al detectar un obstáculo frontal. |
| **`roombaadri.py`** | Modo de navegación autónoma que evita obstáculos, similar al comportamiento de un robot aspirador. |
| **`Aviso_oscuridad.py`** | Activa la bocina (buzzer) automáticamente cuando las fotorresistencias detectan falta de luz. |

---

## 🧠 Clase Robot (`robot.py`)

La clase `Robot` es el motor principal del software. Organiza el control mediante métodos de movimiento y lectura de sensores en hilos (multithreading).

### 🎮 Movimientos Disponibles
Gracias a las ruedas Mecanum, el robot soporta una amplia gama de maniobras:

* **Direccionales:** `forward`, `backward`, `stop`.
* **Giros:** `turn_right`, `counterclockwise_turn`.
* **Laterales:** `right_lateral_movement`, `left_lateral_movement`.
* **Diagonales:** `forward_left_diagonal_movement`, `forward_right_diagonal_movement`, `backward_left_diagonal_movement`, `backward_right_diagonal_movement`.
* **Especiales:** `clockwise_orbit`, `counter_clockwise_orbit`, `free`.



### 📡 Gestión de Sensores (Threads)
El robot actualiza constantemente sus variables de estado mediante hilos independientes:

1.  **`update_ultrasonic`**: Actualiza la variable `distance` (distancia en cm).
2.  **`update_adc`**: Lee el diccionario `adc_readings` con datos de luz (`left_light`, `right_light`) y voltaje de `battery`.
3.  **`update_infrared`**: Lee el diccionario `infrared_readings` para detección de líneas (`left`, `center`, `right`).

### 🛡 Sistema de Seguridad Activa
El método **`antichoque`** (controlado por la variable `enable_antichoque`) actúa como un sistema de asistencia:
* **Parada de emergencia:** Si la distancia es `< 30 cm`.
* **Reducción de velocidad:** Si la distancia está entre `30` y `60 cm`.

---