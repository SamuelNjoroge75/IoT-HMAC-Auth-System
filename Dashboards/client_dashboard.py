import subprocess, threading, time, webbrowser, os
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app  = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent

SCRIPTS = {
    "iot":      BASE_DIR / "IoT_device.py",
    "hmac_iot": BASE_DIR / "HMAC-IoT_device.py",
}

_output: dict[str, list[str]] = {"iot": [], "hmac_iot": []}
_procs:  dict[str, subprocess.Popen] = {}
_lock = threading.Lock()


def stream_output(name, proc):
    for raw in proc.stdout:
        line = raw.decode(errors="replace").rstrip()
        if line:
            _output[name].append(line)
            if len(_output[name]) > 200:
                _output[name] = _output[name][-200:]


def is_running(name):
    with _lock:
        p = _procs.get(name)
        return p is not None and p.poll() is None


@app.route("/")
def index():
    return render_template("IoT.html")


@app.route("/api/status")
def status():
    return jsonify({
        "running": {k: is_running(k) for k in SCRIPTS},
        "line_counts": {k: len(v) for k, v in _output.items()},
    })


@app.route("/api/output/<name>")
def get_output(name):
    if name not in _output:
        return jsonify({"error": "unknown"}), 404
    return jsonify({"lines": _output[name][-80:]})


@app.route("/api/run/<name>", methods=["POST"])
def run_script(name):
    if name not in SCRIPTS:
        return jsonify({"error": "unknown"}), 400
    if is_running(name):
        return jsonify({"status": "already_running"})
    script = SCRIPTS[name]
    if not script.exists():
        return jsonify({"error": f"Script not found: {script}"}), 404
    _output[name].clear()
    _output[name].append(f"[dashboard] Starting {script.name}...")
    with _lock:
        p = subprocess.Popen(
            ["python3", str(script)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        _procs[name] = p
    t = threading.Thread(target=stream_output, args=(name, p), daemon=True)
    t.start()
    return jsonify({"status": "started", "pid": p.pid})


@app.route("/api/clear/<name>", methods=["POST"])
def clear(name):
    if name in _output:
        _output[name].clear()
    return jsonify({"status": "cleared"})


def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://<device's IP Address>:8081")


if __name__ == "__main__":
    print("=" * 55)
    print("  IoT Authentication Security Project — IoT Device Dashboard")
    print("  Opening browser at http://<device's IP Address>:8081 ...")
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="10.10.10.5", port=8081, debug=False)
