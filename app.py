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
            self.adc_readings = {'left_light': 0, 'right_light': 0, 'battery': 0}
            self.infrared_readings = {'left': 0, 'center': 0, 'right': 0}
            self._running = True
            
            # Hilos de simulación
            threading.Thread(target=self._simulate_sensor, daemon=True).start()
            threading.Thread(target=self._simulate_adc, daemon=True).start()
            threading.Thread(target=self._simulate_infra, daemon=True).start()

        def _simulate_sensor(self):
            while self._running:
                self.distance = random.uniform(5.0, 50.0)
                time.sleep(1)

        def _simulate_adc(self):
            while self._running:
                self.adc_readings['left_light'] = random.randint(100, 800)
                self.adc_readings['right_light'] = random.randint(100, 800)
                self.adc_readings['battery'] = random.uniform(7.0, 8.4)
                time.sleep(0.5)

        def _simulate_infra(self):
            while self._running:
                self.infrared_readings['left'] = random.choice([0, 1])
                self.infrared_readings['center'] = random.choice([0, 1])
                self.infrared_readings['right'] = random.choice([0, 1])
                time.sleep(0.5)

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

if ROBOT_REAL:
    time.sleep(0.5)

try:
    robot_controller = Robot()
except Exception as e:
    print(f"Error crítico al inicializar el Robot: {e}")
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
        
        h1 { color: var(--neon-orange); letter-spacing: 2px; text-transform: uppercase; font-weight: 300; margin-bottom: 20px; }
        h1 b { font-weight: 800; }

        .container { max-width: 1000px; width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

        .top-stats {
            grid-column: span 2;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            width: 100%;
            margin-bottom: 10px;
        }

        .stat-card { 
            background: var(--panel-bg); 
            padding: 15px; 
            border-radius: 12px; 
            border-bottom: 4px solid #333;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stat-label { font-size: 0.7rem; color: #888; text-transform: uppercase; font-weight: bold; margin-bottom: 5px; }
        .stat-value { font-size: 1.4rem; font-weight: 800; color: #fff; font-family: monospace; }
        
        .infra-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 5px;
        }
        .infra-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #333;
            border: 1px solid #444;
        }
        .infra-dot.active {
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }

        .card { 
            background: var(--panel-bg); 
            padding: 20px; 
            border-radius: 15px; 
            border: 1px solid #333;
            display: flex;
            flex-direction: column;
        }
        h2 { font-size: 0.9rem; color: var(--neon-orange); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 0; text-transform: uppercase; }

        .grid-controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 20px; }
        .btn { 
            background: #2a2a2a; 
            color: white; 
            border: 1px solid #444; 
            padding: 12px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 1.1rem;
            font-weight: bold; 
            transition: 0.2s;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .btn:active { background: var(--neon-orange); color: black; transform: scale(0.95); }
        .btn-stop { background: var(--danger); border: none; font-size: 0.8rem; font-weight: 900; }
        .btn-reset { font-size: 0.65rem; color: #888; }

        .motor-row { display: flex; align-items: center; gap: 10px; margin: 8px 0; background: #222; padding: 8px; border-radius: 8px; }
        .motor-label { width: 35px; font-weight: bold; color: #777; font-size: 0.75rem; }
        input[type=range] { flex: 1; accent-color: var(--neon-orange); cursor: pointer; }
        .input-val { 
            width: 65px; background: #111; border: 1px solid #444; 
            color: var(--neon-orange); font-family: monospace; font-weight: bold; 
            text-align: right; padding: 4px; border-radius: 4px; font-size: 0.85rem;
        }

        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

    <h1>Robot <b>OS</b></h1>

    <div class="container">
        <!-- Panel de Sensores Superior -->
        <div class="top-stats">
            <div id="dist-card" class="stat-card">
                <div class="stat-label">📡 Distancia</div>
                <div class="stat-value"><span id="dist-val">--</span><small style="font-size: 0.7rem">cm</small></div>
            </div>
            <div class="stat-card" style="border-color: var(--success)">
                <div class="stat-label">🔋 Batería</div>
                <div class="stat-value"><span id="batt-val">--</span><small style="font-size: 0.7rem">V</small></div>
            </div>
            <div class="stat-card" style="border-color: var(--warning)">
                <div class="stat-label">💡 Luz (L / R)</div>
                <div class="stat-value" style="font-size: 1.1rem">
                    <span id="light-l-val">--</span> / <span id="light-r-val">--</span>
                </div>
            </div>
            <div class="stat-card" style="border-color: #9b59b6">
                <div class="stat-label">🛤️ Infrarrojos</div>
                <div class="infra-container">
                    <div id="ir-left" class="infra-dot" title="Izquierda"></div>
                    <div id="ir-center" class="infra-dot" title="Centro"></div>
                    <div id="ir-right" class="infra-dot" title="Derecha"></div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Movimientos Rápidos | <span id="status-display">Cargando...</span></h2>
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
                <div class="motor-label" style="width: 80px">CRUCERO</div>
                <input type="range" id="global-speed-slider" min="0" max="4095" value="600" oninput="syncInputs('global-speed', this.value, true)">
                <input type="number" id="global-speed-num" class="input-val" value="600" oninput="syncInputs('global-speed', this.value, false)">
            </div>
        </div>

        <div class="card">
            <h2>Motores Individuales</h2>
            <div id="motor-sliders"></div>
            <button class="btn" style="background: var(--success); margin-top: 10px; border:none" onclick="applyPotency()">APLICAR PWM</button>
        </div>
    </div>

    <script>
        const motorNames = { 1: "FL", 2: "RL", 3: "FR", 4: "RR" };
        const sliderContainer = document.getElementById('motor-sliders');
        for(let i=1; i<=4; i++) {
            sliderContainer.innerHTML += `
                <div class="motor-row">
                    <div class="motor-label">${motorNames[i]}</div>
                    <input type="range" id="m${i}-slider" min="-4095" max="4095" value="0" oninput="syncInputs('m${i}', this.value, true)">
                    <input type="number" id="m${i}-num" class="input-val" value="0" oninput="syncInputs('m${i}', this.value, false)">
                </div>`;
        }

        function syncInputs(idPrefix, val, isFromSlider) {
            const numInput = document.getElementById(idPrefix + '-num');
            const sliderInput = document.getElementById(idPrefix + '-slider');
            if (isFromSlider) numInput.value = val; else sliderInput.value = val;
            if (idPrefix === 'global-speed') updateGlobalSpeed(val);
        }

        async function updateGlobalSpeed(val) {
            try { await fetch('/set_global_speed', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({speed: parseInt(val) || 0})
            }); } catch(e) {}
        }

        async function apiMove(cmd) {
            try { await fetch('/move/' + cmd, { method: 'POST' }); } catch(e) {}
        }

        async function applyPotency() {
            const s = [1,2,3,4].map(i => document.getElementById(`m${i}-num`).value);
            try { await fetch(`/free_move?s1=${s[0]}&s2=${s[1]}&s3=${s[2]}&s4=${s[3]}`, {method: 'POST'}); } catch(e) {}
        }

        function resetUI() {
            for(let i=1; i<=4; i++) {
                syncInputs('m' + i, 0, true);
            }
            const defaultSpeed = 600;
            syncInputs('global-speed', defaultSpeed, true);
            apiMove('stop');
        }

        setInterval(async () => {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                
                const distEl = document.getElementById('dist-val');
                const distCard = document.getElementById('dist-card');
                const statusEl = document.getElementById('status-display');
                const dist = data.distance;

                // Lógica de colores para Distancia
                distEl.innerText = dist.toFixed(1);
                if (dist > 30) {
                    distCard.style.borderColor = "var(--info)";
                    distEl.style.color = "var(--info)";
                } else if (dist <= 30 && dist > 15) {
                    distCard.style.borderColor = "var(--warning)";
                    distEl.style.color = "var(--warning)";
                } else {
                    distCard.style.borderColor = "var(--danger)";
                    distEl.style.color = "var(--danger)";
                }

                // Lógica de colores para Estado
                statusEl.innerText = data.status;
                if (data.status === "Parado") {
                    statusEl.style.color = "var(--danger)";
                } else {
                    statusEl.style.color = "var(--success)";
                }

                document.getElementById('batt-val').innerText = data.adc.battery.toFixed(2);
                document.getElementById('light-l-val').innerText = data.adc.left_light;
                document.getElementById('light-r-val').innerText = data.adc.right_light;

                // Infrarrojos
                document.getElementById('ir-left').className = 'infra-dot' + (data.infrared.left ? ' active' : '');
                document.getElementById('ir-center').className = 'infra-dot' + (data.infrared.center ? ' active' : '');
                document.getElementById('ir-right').className = 'infra-dot' + (data.infrared.right ? ' active' : '');

            } catch(e) {}
        }, 400);

        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT') return;
            const map = { 
                'ArrowUp':'forward','w':'forward',
                'ArrowDown':'backward','s':'backward',
                'ArrowLeft':'left','a':'left',
                'ArrowRight':'right','d':'right',
                'q':'lateral_left','e':'lateral_right',
                'z':'rotate_ccw', 'x':'rotate_cw',
                ' ':'stop'
            };
            if (map[e.key]) apiMove(map[e.key]);
        });
        document.addEventListener('keyup', (e) => {
            if (e.target.tagName === 'INPUT') return;
            const controls = ['w','s','a','d','q','e','z','x','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'];
            if (controls.includes(e.key)) apiMove('stop');
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
    return jsonify({"status": "ok"})

@app.route('/move/<direction>', methods=['POST'])
def move_robot(direction):
    global current_global_speed, current_status
    speed = current_global_speed
    status_map = {
        'forward': "Adelante", 'backward': "Atrás", 'left': "Giro Izquierda",
        'right': "Giro Derecha", 'stop': "Parado", 'lateral_left': "Lateral Izquierda",
        'lateral_right': "Lateral Derecha", 'diag_fl': "Diagonal FL",
        'diag_fr': "Diagonal FR", 'diag_bl': "Diagonal RL", 'diag_br': "Diagonal RR",
        'rotate_cw': "Rotación CW", 'rotate_ccw': "Rotación CCW"
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
    s1 = int(request.args.get('s1', 0)); s2 = int(request.args.get('s2', 0))
    s3 = int(request.args.get('s3', 0)); s4 = int(request.args.get('s4', 0))
    current_status = "Manual" if (s1 or s2 or s3 or s4) else "Parado"
    robot_controller.free(s1, s2, s3, s4)
    return jsonify({"status": "ok"})

@app.route('/status')
def status():
    return jsonify({
        "distance": getattr(robot_controller, 'distance', 0),
        "status": current_status,
        "adc": getattr(robot_controller, 'adc_readings', {}),
        "infrared": getattr(robot_controller, 'infrared_readings', {})
    })

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    finally:
        if hasattr(robot_controller, 'stop'): robot_controller.stop()
        if hasattr(robot_controller, 'close'): robot_controller.close()