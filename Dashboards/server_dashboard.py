import os, json, subprocess, threading, time, webbrowser
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app  = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent

SCRIPTS = {
    "vulnerable": BASE_DIR / "Vulnerable_server.py",
    "hmac":       BASE_DIR / "HMAC_server.py",
}

LOG_FILES = {
    "vulnerable": BASE_DIR / "Vulnerable_system.log",
    "hmac":       BASE_DIR / "HMAC_system.log",
}

# Process store + stdout capture buffers
_procs:  dict[str, subprocess.Popen] = {}
_output: dict[str, list[str]] = {"vulnerable": [], "hmac": []}
_lock   = threading.Lock()


# ── HELPERS ─────────────────────────────────────────────────

def stream_output(name, proc):
    """Read subprocess stdout line by line into the buffer."""
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


def tail(path: Path, n=80):
    if not path.exists():
        return []
    lines = path.read_text(errors="replace").splitlines()
    return lines[-n:]


def parse_log(path: Path):
    """Count auth attempts from server log."""
    accepted = rejected = 0
    if not path.exists():
        return {"accepted": 0, "rejected": 0, "total": 0}
    for line in path.read_text(errors="replace").splitlines():
        ll = line.lower()
        if "authentication successful" in ll:
            accepted += 1
        if "unauthorized" in ll or "rejected" in ll or "missing" in ll or "mismatch" in ll:
            rejected += 1
    return {"accepted": accepted, "rejected": rejected, "total": accepted + rejected}


# ── ROUTES ───────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("server.html")


@app.route("/api/status")
def status():
    vuln_stats = parse_log(LOG_FILES["vulnerable"])
    hmac_stats = parse_log(LOG_FILES["hmac"])
    return jsonify({
        "services": {
            "vulnerable": is_running("vulnerable"),
            "hmac":       is_running("hmac"),
        },
        "vulnerable_stats": vuln_stats,
        "hmac_stats":       hmac_stats,
    })


@app.route("/api/logs/<name>")
def get_log(name):
    path = LOG_FILES.get(name)
    if not path:
        return jsonify({"error": "unknown"}), 404
    return jsonify({"lines": tail(path)})


@app.route("/api/output/<name>")
def get_output(name):
    if name not in _output:
        return jsonify({"error": "unknown"}), 404
    # Return stdout buffer only — this is the script's print() output,
    # which is distinct from the .log file shown in Server Auth Logs.
    return jsonify({"lines": _output[name][-80:]})


@app.route("/api/start/<name>", methods=["POST"])
def start(name):
    if name not in SCRIPTS:
        return jsonify({"error": "unknown"}), 400
    if is_running(name):
        return jsonify({"status": "already_running"})
    script = SCRIPTS[name]
    if not script.exists():
        return jsonify({"error": f"Script not found: {script}"}), 404

    _output[name].clear()
    _output[name].append(f"[dashboard] Starting {script.name}...")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"   # ensures print() output isn't held in buffer

    with _lock:
        p = subprocess.Popen(
            ["python3", "-u", str(script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
        _procs[name] = p

    t = threading.Thread(target=stream_output, args=(name, p), daemon=True)
    t.start()
    return jsonify({"status": "started", "pid": p.pid})


@app.route("/api/stop/<name>", methods=["POST"])
def stop(name):
    with _lock:
        p = _procs.get(name)
        if p and p.poll() is None:
            p.terminate()
            _procs[name] = None
            return jsonify({"status": "stopped"})
    return jsonify({"status": "not_running"})


@app.route("/api/clear", methods=["POST"])
def clear():
    for path in LOG_FILES.values():
        if path.exists():
            path.write_text("")
    for key in _output:
        _output[key].clear()
    return jsonify({"status": "cleared"})


# ── MAIN ─────────────────────────────────────────────────────

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://10.10.10.1:8080")

if __name__ == "__main__":
    print("=" * 55)
    print("  IoT Authentication Security Project — Server Dashboard")
    print("  Opening browser at http://10.10.10.1:8080 ...")
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="10.10.10.1", port=8080, debug=False)