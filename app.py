from flask import Flask, render_template_string, request, jsonify
import time
import threading
import random
import sys

# Intentamos importar la clase Robot del archivo del usuario (robot.py)
try:
    from robot import Robot
    ROBOT_REAL = True
    print("Modo: ROBOT REAL (Librerías encontradas)")
except ImportError:
    ROBOT_REAL = False
    print("Modo: SIMULACIÓN (Ejecutando sin hardware Freenove)")
    
    class Robot:
        def __init__(self): 
            self.distance = 0
            self._running = True
            self.thread = threading.Thread(target=self._simulate_sensor, daemon=True)
            self.thread.start()

        def _simulate_sensor(self):
            while self._running:
                self.distance = random.uniform(5.0, 50.0)
                time.sleep(1)

        def forward(self, speed=600): print(f"Mock: Adelante {speed}")
        def backward(self, speed=600): print(f"Mock: Atrás {speed}")
        def stop(self): print("Mock: Parar")
        def turn_left(self, speed=600): print(f"Mock: Girar Izq {speed}")
        def turn_right(self, speed=600): print(f"Mock: Girar Der {speed}")
        def right_lateral_movement(self, speed=600): print(f"Mock: Lateral Der {speed}")
        def left_lateral_movement(self, speed=600): print(f"Mock: Lateral Izq {speed}")
        def forward_left_diagonal_movement(self, speed=600): print("Mock: Diagonal Izq-Adelante")
        def forward_right_diagonal_movement(self, speed=600): print("Mock: Diagonal Der-Adelante")
        def backward_left_diagonal_movement(self, speed=600): print("Mock: Diagonal Izq-Atrás")
        def backward_right_diagonal_movement(self, speed=600): print("Mock: Diagonal Der-Atrás")
        def clockwise_turn(self, speed=600): print("Mock: Rotar Horario")
        def counterclockwise_turn(self, speed=600): print("Mock: Rotar Anti-Horario")
        def free(self, s1, s2, s3, s4): print(f"Mock: Motores libres FL:{s1} RL:{s2} FR:{s3} RR:{s4}")
        def close(self): self._running = False

app = Flask(__name__)

# Pequeña pausa para asegurar que los pines se liberen de procesos anteriores
if ROBOT_REAL:
    time.sleep(0.5)

try:
    robot_controller = Robot()
except Exception as e:
    print(f"Error crítico al inicializar el Robot: {e}")
    print("Sugerencia: Ejecuta 'sudo killall python3' si el puerto GPIO está ocupado.")
    sys.exit(1)

current_global_speed = 600 
current_status = "Parado"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Robot Control Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { 
            --neon-orange: #ff8c00; 
            --bg-dark: #0f0f0f; 
            --panel-bg: #1a1a1a; 
            --success: #2ecc71; 
            --danger: #e74c3c; 
            --warning: #f39c12;
            --info: #3498db; 
        }
        
        body { 
            font-family: 'Segoe UI', Roboto, sans-serif; 
            background: var(--bg-dark); 
            color: #eee; 
            margin: 0; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        
        h1 { color: var(--neon-orange); letter-spacing: 2px; text-transform: uppercase; font-weight: 300; margin-bottom: 30px; }
        h1 b { font-weight: 800; }

        .container { max-width: 900px; width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

        .top-panels {
            grid-column: span 2;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            width: 100%;
        }

        .header-card { 
            background: var(--panel-bg); 
            padding: 20px; 
            border-radius: 15px; 
            border-bottom: 4px solid var(--info);
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
        }

        .dist-label { font-size: 0.8rem; color: #888; text-transform: uppercase; margin-bottom: 5px; font-weight: bold; }
        .dist-value { font-size: 2.5rem; font-weight: 800; color: var(--info); font-family: monospace; }
        
        .status-text { font-size: 1.5rem; font-weight: 700; margin-top: 10px; text-transform: uppercase; min-height: 1.8rem; }

        .card { 
            background: var(--panel-bg); 
            padding: 20px; 
            border-radius: 15px; 
            border: 1px solid #333;
            display: flex;
            flex-direction: column;
        }
        h2 { font-size: 1rem; color: var(--neon-orange); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 0; }

        .grid-controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
        .btn { 
            background: #2a2a2a; 
            color: white; 
            border: 1px solid #444; 
            padding: 15px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 1.2rem;
            font-weight: bold; 
            transition: 0.2s;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .btn:hover { border-color: var(--neon-orange); }
        .btn:active { background: var(--neon-orange); color: black; transform: scale(0.95); }
        .btn-stop { background: var(--danger); border: none; font-size: 0.8rem; }
        .btn-stop:hover { background: #c0392b; }
        .btn-reset { font-size: 0.7rem; }

        .motor-row { display: flex; align-items: center; gap: 15px; margin: 15px 0; background: #222; padding: 10px; border-radius: 8px; }
        .motor-label { width: 40px; font-weight: bold; color: #777; font-size: 0.8rem; }
        .speed-label-full { flex: 1; font-weight: bold; color: var(--neon-orange); text-transform: uppercase; font-size: 0.75rem; }
        
        input[type=range] { flex: 1; accent-color: var(--neon-orange); cursor: pointer; }
        .motor-val { width: 60px; text-align: right; color: var(--neon-orange); font-family: monospace; font-weight: bold; }

        .btn-apply { 
            width: 100%; 
            background: var(--success); 
            color: white; 
            border: none; 
            padding: 18px; 
            border-radius: 8px; 
            font-size: 1rem; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2);
            transition: 0.2s;
            margin-top: auto;
        }

        @media (max-width: 768px) { 
            .container { grid-template-columns: 1fr; } 
            .top-panels { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <h1>Robot <b>OS</b></h1>

    <div class="container">
        <div class="top-panels">
            <div class="header-card" id="dist-card">
                <div class="dist-label">📡 Ultrasonidos</div>
                <div class="dist-value">
                    <span id="dist-display">--</span> 
                    <small style="font-size: 1rem; color: #555;">cm</small>
                </div>
            </div>

            <div class="header-card" id="status-card">
                <div class="dist-label">🤖 Estado del Sistema</div>
                <div class="status-text" id="status-display">Cargando...</div>
            </div>
        </div>

        <div class="card">
            <h2>Movimientos Rápidos</h2>
            <div class="grid-controls">
                <button class="btn" onclick="apiMove('diag_fl')">◤</button>
                <button class="btn" onclick="apiMove('forward')">▲</button>
                <button class="btn" onclick="apiMove('diag_fr')">◥</button>
                
                <button class="btn" onclick="apiMove('lateral_left')">◀</button>
                <button class="btn btn-stop" onclick="apiMove('stop')">STOP</button>
                <button class="btn" onclick="apiMove('lateral_right')">▶</button>
                
                <button class="btn" onclick="apiMove('diag_bl')">◣</button>
                <button class="btn" onclick="apiMove('backward')">▼</button>
                <button class="btn" onclick="apiMove('diag_br')">◢</button>
                
                <button class="btn" onclick="apiMove('rotate_ccw')">↺</button>
                <button class="btn btn-reset" onclick="resetUI()">RESET</button>
                <button class="btn" onclick="apiMove('rotate_cw')">↻</button>
            </div>

            <div class="motor-row" style="background: #2a2a2a; border: 1px solid #444;">
                <div class="speed-label-full">Velocidad crucero</div>
                <input type="range" id="global-speed" min="0" max="4095" value="600" oninput="updateGlobalSpeed(this.value)">
                <div class="motor-val" id="global-speed-val">600</div>
            </div>
        </div>

        <div class="card">
            <h2>Motores Individuales (-4095 a 4095)</h2>
            <div id="motor-sliders"></div>
            <button class="btn-apply" onclick="applyPotency()">APLICAR CONFIGURACIÓN</button>
        </div>
    </div>

    <script>
        const motorNames = { 1: "FL", 2: "RL", 3: "FR", 4: "RR" };

        const sliderContainer = document.getElementById('motor-sliders');
        for(let i=1; i<=4; i++) {
            sliderContainer.innerHTML += `
                <div class="motor-row">
                    <div class="motor-label" title="Motor ${i}">${motorNames[i]}</div>
                    <input type="range" id="m${i}" min="-4095" max="4095" value="0" oninput="document.getElementById('v${i}').innerText=this.value">
                    <div class="motor-val" id="v${i}">0</div>
                </div>`;
        }

        async function updateGlobalSpeed(val) {
            document.getElementById('global-speed-val').innerText = val;
            try {
                await fetch('/set_global_speed', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({speed: parseInt(val)})
                });
            } catch(e) { console.error(e); }
        }

        async function apiMove(cmd) {
            try { await fetch('/move/' + cmd, { method: 'POST' }); } catch(e) { console.error(e); }
        }

        async function applyPotency() {
            const s1 = document.getElementById('m1').value;
            const s2 = document.getElementById('m2').value;
            const s3 = document.getElementById('m3').value;
            const s4 = document.getElementById('m4').value;
            try { await fetch(`/free_move?s1=${s1}&s2=${s2}&s3=${s3}&s4=${s4}`, {method: 'POST'}); } catch(e) { console.error(e); }
        }

        function resetUI() {
            for(let i=1; i<=4; i++) {
                document.getElementById('m'+i).value = 0;
                document.getElementById('v'+i).innerText = 0;
            }
            const defaultSpeed = 600;
            const globalSlider = document.getElementById('global-speed');
            globalSlider.value = defaultSpeed;
            updateGlobalSpeed(defaultSpeed);
            apiMove('stop');
        }

        setInterval(async () => {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                const distDisplay = document.getElementById('dist-display');
                const statusDisplay = document.getElementById('status-display');
                const distCard = document.getElementById('dist-card');
                const statusCard = document.getElementById('status-card');
                const dist = data.distance;

                distDisplay.innerText = dist.toFixed(1);

                if (dist > 30) {
                    distDisplay.style.color = "var(--info)";
                    distCard.style.borderColor = "var(--info)";
                } else if (dist <= 30 && dist > 15) {
                    distDisplay.style.color = "var(--warning)";
                    distCard.style.borderColor = "var(--warning)";
                } else {
                    distDisplay.style.color = "var(--danger)";
                    distCard.style.borderColor = "var(--danger)";
                }

                statusDisplay.innerText = data.status;
                if (data.status === "Parado") {
                    statusDisplay.style.color = "var(--danger)";
                    statusCard.style.borderColor = "var(--danger)";
                } else {
                    statusDisplay.style.color = "var(--success)";
                    statusCard.style.borderColor = "var(--success)";
                }

            } catch(e) { console.error(e); }
        }, 400);

        document.addEventListener('keydown', (e) => {
            if (e.repeat) return;
            const map = {
                'ArrowUp': 'forward', 'w': 'forward',
                'ArrowDown': 'backward', 's': 'backward',
                'ArrowLeft': 'left', 'a': 'left',
                'ArrowRight': 'right', 'd': 'right',
                'q': 'lateral_left', 'e': 'lateral_right',
                ' ': 'stop'
            };
            if (map[e.key]) apiMove(map[e.key]);
        });
        document.addEventListener('keyup', (e) => {
            if (['w','s','a','d','q','e','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) apiMove('stop');
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/set_global_speed', methods=['POST'])
def set_global_speed():
    global current_global_speed
    data = request.get_json()
    current_global_speed = data.get('speed', 600)
    return jsonify({"status": "ok", "speed": current_global_speed})

@app.route('/move/<direction>', methods=['POST'])
def move_robot(direction):
    global current_global_speed, current_status
    speed = current_global_speed
    status_map = {
        'forward': "Adelante", 'backward': "Atrás", 'left': "Giro Izquierda",
        'right': "Giro Derecha", 'stop': "Parado", 'lateral_left': "Lateral Izquierda",
        'lateral_right': "Lateral Derecha", 'diag_fl': "Diagonal Front-Izq",
        'diag_fr': "Diagonal Front-Der", 'diag_bl': "Diagonal Atrás-Izq",
        'diag_br': "Diagonal Atrás-Der", 'rotate_cw': "Rotación Horaria",
        'rotate_ccw': "Rotación Anti-Horaria"
    }
    current_status = status_map.get(direction, "En marcha")
    if direction == 'forward': robot_controller.forward(speed)
    elif direction == 'backward': robot_controller.backward(speed)
    elif direction == 'left': robot_controller.turn_left(speed)
    elif direction == 'right': robot_controller.turn_right(speed)
    elif direction == 'stop': robot_controller.stop()
    elif direction == 'lateral_left': robot_controller.left_lateral_movement(speed)
    elif direction == 'lateral_right': robot_controller.right_lateral_movement(speed)
    elif direction == 'diag_fl': robot_controller.forward_left_diagonal_movement(speed)
    elif direction == 'diag_fr': robot_controller.forward_right_diagonal_movement(speed)
    elif direction == 'diag_bl': robot_controller.backward_left_diagonal_movement(speed)
    elif direction == 'diag_br': robot_controller.backward_right_diagonal_movement(speed)
    elif direction == 'rotate_cw': robot_controller.clockwise_turn(speed)
    elif direction == 'rotate_ccw': robot_controller.counterclockwise_turn(speed)
    return jsonify({"status": "ok"})

@app.route('/free_move', methods=['POST'])
def free_move():
    global current_status
    s1 = int(request.args.get('s1', 0))
    s2 = int(request.args.get('s2', 0))
    s3 = int(request.args.get('s3', 0))
    s4 = int(request.args.get('s4', 0))
    current_status = "Parado" if (s1==s2==s3==s4==0) else "Manual (Personalizado)"
    robot_controller.free(s1, s2, s3, s4)
    return jsonify({"status": "ok"})

@app.route('/status')
def status():
    global current_status
    dist = getattr(robot_controller, 'distance', -1)
    return jsonify({"distance": dist, "status": current_status})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    finally:
        # Aseguramos que al cerrar el servidor se intenten liberar recursos
        print("Cerrando controlador...")
        if hasattr(robot_controller, 'stop'):
            robot_controller.stop()
        if hasattr(robot_controller, 'close'):
            robot_controller.close()