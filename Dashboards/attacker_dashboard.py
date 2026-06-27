import argparse, subprocess, threading, time, webbrowser, requests as req_lib
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app  = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent

SCRIPTS = {
    "attacker":    BASE_DIR / "attacker.py",
    "hmac_attack": BASE_DIR / "HMAC_attacker.py",
    "nmap":        BASE_DIR / "Nmap_discovery.py",
}

LOG_FILES = {
    "attacker":    BASE_DIR / "Attacker.log",
    "hmac_attack": BASE_DIR / "HMAC_Attacker.log",
}

_output: dict[str, list[str]] = {"attacker": [], "hmac_attack": [], "nmap": []}
_procs:  dict[str, subprocess.Popen] = {}
_lock = threading.Lock()
_server_url = "http://<server's IP Address>:5000"   # Server dashboard for log forwarding


def stream_output(name, proc):
    for raw in proc.stdout:
        line = raw.decode(errors="replace").rstrip()
        if line:
            _output[name].append(line)
            if len(_output[name]) > 300:
                _output[name] = _output[name][-300:]
    if _server_url and name in LOG_FILES:
        forward_log(name)


def forward_log(name):
    path = LOG_FILES.get(name)
    if not path or not path.exists() or not _server_url:
        return
    lines = path.read_text(errors="replace").splitlines()
    if not lines:
        return
    try:
        req_lib.post(f"{_server_url}/api/ingest/logs", json={
            "agent_id": "attacker_vm",
            "log": name,
            "lines": lines
        }, timeout=5)
    except Exception:
        pass


def is_running(name):
    with _lock:
        p = _procs.get(name)
        return p is not None and p.poll() is None


def parse_attack_log(path: Path):
    if not path.exists():
        return {"total": 0, "success": 0, "blocked": 0, "rate": 0.0}
    success = total = 0
    for line in path.read_text(errors="replace").splitlines():
        if "Attempt" in line and ("SUCCESS" in line or "BLOCKED" in line or "FAILED" in line):
            total += 1
            if "SUCCESS" in line:
                success += 1
    blocked = total - success
    rate = round((success / total * 100), 1) if total else 0.0
    return {"total": total, "success": success, "blocked": blocked, "rate": rate}


@app.route("/")
def index():
    return render_template("attacker.html")


@app.route("/api/status")
def status():
    p1 = parse_attack_log(LOG_FILES["attacker"])
    p2 = parse_attack_log(LOG_FILES["hmac_attack"])
    return jsonify({
        "running": {k: is_running(k) for k in SCRIPTS},
        "phase1":  p1,
        "phase2":  p2,
        "improvement": round(p1["rate"] - p2["rate"], 1),
        "server_linked": _server_url is not None,
    })


@app.route("/api/output/<name>")
def get_output(name):
    if name not in _output:
        return jsonify({"error": "unknown"}), 404
    return jsonify({"lines": _output[name][-100:]})


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
    if name in LOG_FILES and LOG_FILES[name].exists():
        LOG_FILES[name].write_text("")
    with _lock:
        p = subprocess.Popen(
            ["python3", str(script)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        _procs[name] = p
    t = threading.Thread(target=stream_output, args=(name, p), daemon=True)
    t.start()
    return jsonify({"status": "started", "pid": p.pid})


@app.route("/api/logs/<name>")
def get_log(name):
    path = LOG_FILES.get(name)
    if not path:
        return jsonify({"error": "unknown"}), 404
    lines = path.read_text(errors="replace").splitlines() if path.exists() else []
    return jsonify({"lines": lines[-80:]})


@app.route("/api/clear", methods=["POST"])
def clear():
    for name in _output:
        _output[name].clear()
    for path in LOG_FILES.values():
        if path.exists():
            path.write_text("")
    return jsonify({"status": "cleared"})


def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://<device's IP Address>:8082")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default=None,
                        help="Override server dashboard URL for log forwarding")
    args = parser.parse_args()
    if args.server:
        _server_url = args.server.rstrip("/")
        print(f"  Log forwarding → {_server_url}")

    print("=" * 55)
    print("  IoT Authentication Security Project — Attacker Dashboard")
    print("  Opening browser at http://<device's IP Address>:8082 ...")
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="10.10.10.24", port=8082, debug=False)
