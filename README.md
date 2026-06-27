# IoT HMAC Authentication System

## Project Overview
This project demonstrates the security weakness of MAC-address-only authentication in IoT device communication and evaluates HMAC-SHA256 as a mitigation. A vulnerable Flask server is first attacked using a forged-MAC impersonation technique, then the same attack is repeated against an HMAC-secured version of the server to measure the security
improvement.

---

## Repository Structure
IoT-HMAC-Auth-System/
├── Phase_1/
│   ├── Vulnerable_server/
│   │   └── Vulnerable_server.py
│   ├── IoT-client/
│   │   └── IoT_device.py
│   ├── attacker/
│   │   ├── Attacker_device.py
│   │   └── Nmap_discovery.py
│   └── Phase1_README.md
├── Phase_2/
│   ├── HMAC-IoT-server/
│   │   ├── HMAC_server.py
│   │   └── key_generator.py
│   ├── HMAC-IoT-client/
│   │   └── HMAC_IoT_device.py
│   ├── Attacker/
│   │   └── HMAC_attacker.py
│   └── Phase2_README.md
├── Evaluation
|   │──security_evaluation.py
│   └── Evaluation_README.md
├── Dashboards
│   ├── server_dashboard.py
│   ├── client_dashboard.py
│   ├── attacker_dashboard.py
│   └── templates/
│   |    ├── server.html
│   |    ├── IoT.html
│   |    └── attacker.html
|   |  
|   └──Dashboards_README.md
└── README.md

---
## Phases

### Phase 1 — Vulnerable Server & Impersonation Attack
A Flask server authenticates IoT devices using only their MAC address.
An attacker uses Nmap to discover the legitimate device's MAC, then sends forged HTTP requests using that address. The server accepts every forged request, proving the vulnerability.

**Result:** ~100% attack success rate

See `Phase_1/Phase1_README.md` for full setup and attack steps.

### Phase 2 — HMAC-Secured Server (Mitigation)
HMAC-SHA256 is added to both the server and client. A pre-shared secret key, never transmitted over the network, is used to sign and verify every request. The same attacker repeats its attack using two bypass methods — all are rejected.

**Result:** 0% attack success rate

See `Phase_2/Phase2_README.md` for full setup and attack steps.

### Security Evaluation (D4)
A comparison script parses both phases' attacker logs and generates a side-by-side table showing the security improvement achieved by HMAC.

See evaluation README for details.

---

## Dashboards
Each VM has a browser-based dashboard for controlling and monitoring scripts without using the terminal directly.

| Dashboard | VM | URL |
|---|---|---|
| server_dashboard.py | Ubuntu Server | http://<server's IP Address>:8080 |
| client_dashboard.py | IoT Device | http://<device's IP Address>:8081 |
| attacker_dashboard.py | Attacker | http://<device's IP Address>:8082 |

To run on each VM:
```bash
pip install flask flask-cors requests
python3 Dashboards/server_dashboard.py     # on Ubuntu Server VM
python3 Dashboards/client_dashboard.py     # on IoT Device VM
python3 Dashboards/attacker_dashboard.py   # on Attacker VM
```

The dashboards allow you to start/stop server scripts, run attack and client scripts, and view live output and logs — all from the browser.

---

## Network Setup
| VM | Role | IP Address |
|---|---|---|
| Ubuntu Server | Flask Server | 10.10.10.1 |
| Kali 1 | Legitimate IoT Client | 10.10.10.2 |
| Kali 2 | Attacker | 10.10.10.3 |

**Network:** VirtualBox Internal Network — IoTLab (`10.10.10.0/24`)

---

## Key Findings
| Metric | Phase 1 (Vulnerable) | Phase 2 (HMAC) |
|---|---|---|
| Attack Success Rate | ~100% | 0% |

Introducing HMAC-SHA256 authentication, combined with timing-safe signature comparison (`hmac.compare_digest()`), eliminated all tested impersonation attack vectors against the IoT authentication system.

---
---

## Author
Samuel — Strathmore University
Computer and Network Security
Supervised by Mr. James Gikera