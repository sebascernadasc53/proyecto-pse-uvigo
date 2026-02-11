from flask import Flask, render_template_string, request, jsonify
import time
import threading
import random
import sys

try:
    from robot import Robot
    ROBOT_REAL = True
    print("Modo: ROBOT REAL")
except ImportError: 
    ROBOT_REAL = False
    print("Modo: SIMULACIÓN")
#Crea la clase robot para simular el funcionamiento de la interfaz   
    class Robot:
        def __init__(self): 
            self.distance = 0
            self.enable_antichoque = False  # Variable añadida
            self.adc_readings = {'left_light': 0, 'right_light': 0, 'battery': 0}
            self.infrared_readings = {'left': 0, 'center': 0, 'right': 0}
            self._running = True
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
        def clockwise_orbit(self): print("Mock: Órbita CW")
        def counter_clockwise_orbit(self): print("Mock: Órbita CCW")
        def free(self, s1, s2, s3, s4): print(f"Mock: Libre FL{s1} RL{s2} FR{s3} RR{s4}")
        def set_servo(self, channel, angle, error=10): print(f"Mock: Servo {channel} a {angle}")
        def close(self): self._running = False
#Final de la creación de la clase simulada
app = Flask(__name__)

#Inicialización del robot
if ROBOT_REAL:
    time.sleep(0.5)

try:
    robot_controller = Robot()
    if ROBOT_REAL:
        robot_controller.enable_antichoque = False # Asegurar estado inicial
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

current_global_speed = 600 
current_status = "Parado"
active_process = None

#Final de la inicialización
#Plantilla de HTML

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Control robot FREENOVE 4WD Mecanum wheels</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { 
            --neon-orange: #ff8c00; --bg-dark: #0f0f0f; --panel-bg: #1a1a1a; 
            --success: #2ecc71; --danger: #e74c3c; --warning: #f39c12;
            --info: #3498db; --purple: #9b59b6;
        }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg-dark); color: #eee; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { max-width: 1200px; width: 100%; display: grid; grid-template-columns: 280px 1fr 1fr; gap: 20px; }
        .top-stats { grid-column: span 3; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; width: 100%; margin-bottom: 10px; }
        .stat-card { background: var(--panel-bg); padding: 15px; border-radius: 12px; border-bottom: 4px solid #333; text-align: center; transition: border-color 0.3s; }
        .stat-label { font-size: 0.7rem; color: #888; text-transform: uppercase; font-weight: bold; }
        .stat-value { font-size: 1.4rem; font-weight: 800; transition: color 0.3s; }
        .card { background: var(--panel-bg); padding: 20px; border-radius: 15px; border: 1px solid #333; }
        h2 { font-size: 0.9rem; color: var(--neon-orange); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 0; text-transform: uppercase; }
        .grid-controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 20px; }
        .btn { background: #2a2a2a; color: white; border: 1px solid #444; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.1s; position: relative; }
        .btn.active { background: var(--neon-orange) !important; color: black !important; border-color: var(--neon-orange) !important; transform: scale(0.98); box-shadow: 0 0 15px rgba(255, 140, 0, 0.4); }
        .btn-stop { background: var(--danger); border: none; font-size: 0.8rem; font-weight: 900; }
        .btn-special { background: #222; color: var(--purple); font-size: 0.8rem; margin-bottom: 8px; width: 100%; border: 1px solid #444; }
        .btn-special:hover { border-color: var(--purple); background: #2a242d; }
        .btn-antichoque { border-color: var(--danger); color: var(--danger); }
        .btn-antichoque.enabled { background: var(--danger); color: white; box-shadow: 0 0 10px rgba(231, 76, 60, 0.4); }
        .motor-row { display: flex; align-items: center; gap: 10px; margin: 8px 0; background: #222; padding: 8px; border-radius: 8px; }
        .input-val { width: 65px; background: #111; border: 1px solid #444; color: var(--neon-orange); text-align: right; padding: 4px; border-radius: 4px; font-size: 0.85rem; }
        input[type=range] { flex: 1; accent-color: var(--neon-orange); cursor: pointer; }
        .infra-dot { width: 12px; height: 12px; border-radius: 50%; background: #333; display: inline-block; }
        .infra-dot.active { background: var(--success); box-shadow: 0 0 8px var(--success); }
        .status-moving { color: var(--success) !important; }
        .status-stopped { color: var(--danger) !important; }
        @media (max-width: 1000px) { .container { grid-template-columns: 1fr; } .top-stats { grid-column: span 1; } }
    </style>
</head>
<body>
    <h1>Robot <b>OS</b></h1>
    <div class="container">
        <div class="top-stats">
            <div id="dist-card" class="stat-card"><div class="stat-label">📡 Distancia</div><div class="stat-value"><span id="dist-val">--</span><small> cm</small></div></div>
            <div class="stat-card" style="border-color: var(--success)"><div class="stat-label">🔋 Batería</div><div class="stat-value"><span id="batt-val">--</span><small> V</small></div></div>
            <div class="stat-card" style="border-color: var(--warning)"><div class="stat-label">💡 Luz</div><div class="stat-value"><span id="light-l-val">--</span> / <span id="light-r-val">--</span></div></div>
            <div class="stat-card" style="border-color: var(--purple)"><div class="stat-label">🛤️ Infrarrojos</div>
                <div style="margin-top:5px"><div id="ir-left" class="infra-dot"></div> <div id="ir-center" class="infra-dot"></div> <div id="ir-right" class="infra-dot"></div></div>
            </div>
        </div>

        <div class="card">
            <h2>Movimientos Especiales</h2>
            <button id="btn-antichoque" class="btn btn-special btn-antichoque" onclick="toggleAntichoque()">🛡️ Antichoque: OFF</button>
            <button id="btn-orbit_cw" class="btn btn-special" onclick="toggleMove('orbit_cw')">🌀 Órbita Horaria</button>
            <button id="btn-orbit_ccw" class="btn btn-special" onclick="toggleMove('orbit_ccw')">🌀 Órbita Antihoraria</button>
            
            <h2 style="margin-top:20px;">Control Servos</h2>
            <div class="motor-row">
                <div style="font-size:0.7rem; width:40px">S0 (H)</div>
                <input type="range" id="s0-slider" min="0" max="180" value="70" oninput="updateServo(0, this.value)">
                <span id="s0-val" class="input-val" style="padding:2px; min-width:30px; text-align:center">70°</span>
            </div>
            <div class="motor-row">
                <div style="font-size:0.7rem; width:40px">S1 (V)</div>
                <input type="range" id="s1-slider" min="70" max="175" value="90" oninput="updateServo(1, this.value)">
                <span id="s1-val" class="input-val" style="padding:2px; min-width:30px; text-align:center">90°</span>
            </div>
            <button class="btn btn-special" style="border-color: var(--info); color: var(--info); margin-top:5px" onclick="centerServos()">🎯 Centrar Cabeza</button>
        </div>

        <div class="card">
            <h2>Control Maestro | <span id="status-display">--</span></h2>
            <div class="grid-controls">
                <button id="btn-diag_fl" class="btn" onclick="toggleMove('diag_fl')">◤</button>
                <button id="btn-forward" class="btn" onclick="toggleMove('forward')">▲</button>
                <button id="btn-diag_fr" class="btn" onclick="toggleMove('diag_fr')">◥</button>
                <button id="btn-lateral_left" class="btn" onclick="toggleMove('lateral_left')">◀</button>
                <button id="btn-stop" class="btn btn-stop" onclick="stopAll()">STOP</button>
                <button id="btn-lateral_right" class="btn" onclick="toggleMove('lateral_right')">▶</button>
                <button id="btn-diag_bl" class="btn" onclick="toggleMove('diag_bl')">◣</button>
                <button id="btn-backward" class="btn" onclick="toggleMove('backward')">▼</button>
                <button id="btn-diag_br" class="btn" onclick="toggleMove('diag_br')">◢</button>
                <button id="btn-rotate_ccw" class="btn" onclick="toggleMove('rotate_ccw')">↺</button>
                <button class="btn" style="font-size:0.6rem; color: var(--warning);" onclick="safeRefresh()">REFRESH</button>
                <button id="btn-rotate_cw" class="btn" onclick="toggleMove('rotate_cw')">↻</button>
            </div>
            <div class="motor-row" style="margin-top:15px">
                <div style="font-size:0.7rem; width:70px">CRUCERO</div>
                <input type="range" id="global-speed-slider" min="0" max="4095" value="600" oninput="syncInputs('global-speed', this.value, true)">
                <input type="number" id="global-speed-num" class="input-val" value="600" oninput="syncInputs('global-speed', this.value, false)">
            </div>
        </div>

        <div class="card">
            <h2>Motores Individuales</h2>
            <div id="motor-sliders"></div>
            <button class="btn" style="background: var(--success); width:100%; margin-top:10px; border:none" onclick="applyPotency()">Aplicar Motores</button>
        </div>
    </div>

    <script>
        const motorNames = { 1: "FL", 2: "RL", 3: "FR", 4: "RR" };
        const sliderContainer = document.getElementById('motor-sliders');
        for(let i=1; i<=4; i++) {
            sliderContainer.innerHTML += `<div class="motor-row">
                <div style="font-size:0.7rem; width:30px">${motorNames[i]}</div>
                <input type="range" id="m${i}-slider" min="-4095" max="4095" value="0" oninput="syncInputs('m${i}', this.value, true)">
                <input type="number" id="m${i}-num" class="input-val" value="0" oninput="syncInputs('m${i}', this.value, false)">
            </div>`;
        }

        let currentActiveToggle = null;

        async function toggleAntichoque() {
            const res = await fetch('/toggle_antichoque', { method: 'POST' });
            const data = await res.json();
            const btn = document.getElementById('btn-antichoque');
            if (data.enabled) {
                btn.classList.add('enabled');
                btn.innerText = "🛡️ Antichoque: ON";
            } else {
                btn.classList.remove('enabled');
                btn.innerText = "🛡️ Antichoque: OFF";
            }
        }

        async function apiMove(cmd) { 
            await fetch('/move/' + cmd, { method: 'POST' }); 
        }

        async function stopAll() {
            if (currentActiveToggle) {
                document.getElementById('btn-' + currentActiveToggle)?.classList.remove('active');
                currentActiveToggle = null;
            }
            await apiMove('stop');
        }

        function toggleMove(cmd) {
            const btn = document.getElementById('btn-' + cmd);
            if (currentActiveToggle === cmd) {
                stopAll();
            } else {
                if (currentActiveToggle) {
                    document.getElementById('btn-' + currentActiveToggle)?.classList.remove('active');
                }
                currentActiveToggle = cmd;
                btn?.classList.add('active');
                apiMove(cmd);
            }
        }

        const keyMap = {
            'ArrowUp': 'forward', 'w': 'forward', 'W': 'forward',
            'ArrowDown': 'backward', 's': 'backward', 'S': 'backward',
            'ArrowLeft': 'left', 'a': 'lateral_left', 'A': 'lateral_left',
            'ArrowRight': 'right', 'd': 'lateral_right', 'D': 'lateral_right',
            'q': 'rotate_ccw', 'Q': 'rotate_ccw',
            'e': 'rotate_cw', 'E': 'rotate_cw',
            ' ': 'stop'
        };

        const keysPressed = new Set();

        document.addEventListener('keydown', (e) => {
            const cmd = keyMap[e.key];
            if (cmd && !keysPressed.has(e.key)) {
                e.preventDefault();
                keysPressed.add(e.key);
                if (currentActiveToggle) {
                    document.getElementById('btn-' + currentActiveToggle)?.classList.remove('active');
                    currentActiveToggle = null;
                }
                apiMove(cmd);
                document.getElementById('btn-' + cmd)?.classList.add('active');
            }
        });

        document.addEventListener('keyup', (e) => {
            const cmd = keyMap[e.key];
            if (cmd) {
                keysPressed.delete(e.key);
                apiMove('stop');
                document.getElementById('btn-' + cmd)?.classList.remove('active');
            }
        });

        function syncInputs(id, val, isSlider) {
            const n = document.getElementById(id + '-num');
            const s = document.getElementById(id + '-slider');
            if (isSlider) n.value = val; else s.value = val;
            if (id === 'global-speed') fetch('/set_global_speed', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({speed:parseInt(val)})});
        }

        function updateServo(channel, angle) {
            document.getElementById(`s${channel}-val`).innerText = angle + "°";
            document.getElementById(`s${channel}-slider`).value = angle;
            fetch(`/set_servo?channel=${channel}&angle=${angle}`, {method:'POST'});
        }

        function centerServos() { updateServo(0, 70); updateServo(1, 90); }
        async function safeRefresh() { await stopAll(); location.reload(); }
        async function applyPotency() {
            const s = [1,2,3,4].map(i => document.getElementById(`m${i}-num`).value);
            await fetch(`/free_move?s1=${s[0]}&s2=${s[1]}&s3=${s[2]}&s4=${s[3]}`, {method: 'POST'});
        }

        setInterval(async () => {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                const distEl = document.getElementById('dist-val');
                const distCard = document.getElementById('dist-card');
                distEl.innerText = data.distance.toFixed(1);
                
                if (data.distance > 30) { distCard.style.borderColor = "var(--info)"; distEl.style.color = "var(--info)"; }
                else if (data.distance > 15) { distCard.style.borderColor = "var(--warning)"; distEl.style.color = "var(--warning)"; }
                else { distCard.style.borderColor = "var(--danger)"; distEl.style.color = "var(--danger)"; }
                
                const statusEl = document.getElementById('status-display');
                statusEl.innerText = data.status;
                statusEl.className = (data.status === "Parado" || data.status.includes("Error")) ? 'status-stopped' : 'status-moving';

                document.getElementById('batt-val').innerText = data.adc.battery.toFixed(2);
                document.getElementById('light-l-val').innerText = data.adc.left_light;
                document.getElementById('light-r-val').innerText = data.adc.right_light;
                ['left','center','right'].forEach(pos => {
                    document.getElementById('ir-'+pos).className = 'infra-dot' + (data.infrared[pos] ? ' active' : '');
                });
            } catch(e) {}
        }, 500);
    </script>
</body>
</html>
"""
#Final plantilla HTML

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/toggle_antichoque', methods=['POST'])
def toggle_antichoque():
    # Cambia el estado en la instancia del controlador
    new_state = not getattr(robot_controller, 'enable_antichoque', False)
    robot_controller.enable_antichoque = new_state
    return jsonify({"status": "ok", "enabled": new_state})

@app.route('/set_global_speed', methods=['POST'])
def set_global_speed():
    global current_global_speed
    current_global_speed = request.get_json().get('speed', 600)
    return jsonify({"status": "ok"})

@app.route('/set_servo', methods=['POST'])
def set_servo_api():
    channel = request.args.get('channel')
    angle = request.args.get('angle')
    if channel is not None and angle is not None:
        robot_controller.set_servo(int(channel), int(angle))
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/move/<direction>', methods=['POST'])
def move_robot(direction):
    global current_global_speed, current_status, active_process
    if active_process and active_process.poll() is None:
        active_process.terminate()
        active_process = None

    status_map = {
        'forward': "Adelante", 'backward': "Atrás", 'stop': "Parado",
        'left': "Giro Izq", 'right': "Giro Der", 'rotate_cw': "Rotación CW",
        'rotate_ccw': "Rotación CCW", 'orbit_cw': "Órbita CW", 'orbit_ccw': "Órbita CCW",
        'lateral_left': "Lateral Izq", 'lateral_right': "Lateral Der",
        'diag_fl': "Diag. FL", 'diag_fr': "Diag. FR", 'diag_bl': "Diag. BL", 'diag_br': "Diag. BR"
    }
    current_status = status_map.get(direction, "Manual")
    
    speed = current_global_speed
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
    elif direction == 'orbit_cw': robot_controller.clockwise_orbit()
    elif direction == 'orbit_ccw': robot_controller.counter_clockwise_orbit()
    return jsonify({"status": "ok"})

@app.route('/free_move', methods=['POST'])
def free_move():
    global current_status
    s = [int(request.args.get(f's{i}', 0)) for i in range(1,5)]
    current_status = "Manual" if any(s) else "Parado"
    robot_controller.free(*s)
    return jsonify({"status": "ok"})

@app.route('/status')
def status():
    return jsonify({
        "distance": getattr(robot_controller, 'distance', 0),
        "status": current_status,
        "adc": getattr(robot_controller, 'adc_readings', {}),
        "infrared": getattr(robot_controller, 'infrared_readings', {}),
        "antichoque": getattr(robot_controller, 'enable_antichoque', False)
    })

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        if active_process: active_process.terminate()
        robot_controller.close()