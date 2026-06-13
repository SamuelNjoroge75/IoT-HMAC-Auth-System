# IoT-HMAC-Auth-System
HMAC-based IoT Authentication System
# Phase 1

## Part 1- Vulnerable IoT Server using Identifier-based Authentication 

### Overview
This phase demonstrates the vulnerability of MAC address-only authentication.
The Flask server accepts any HTTP request that presents a known MAC address
in the `mac-address` header, with no cryptographic verification

### Environment setup
#### Ubuntu server VM
1. Install dependencies: 'pip3 install flask'
2. Run: 'python3 Vulnerable_server.py'
3. Server listens on port 5000

#### Kali 1 VM- Legitimate IoT Client
1. Install dependencies: 'pip3 install requests'
2. Configure 'IoT_device.py' and set 'server_url' to the IP address if the Ubuntu Server.
3. Run: 'python3 IoT_device.py'

### Expected Behaviour
- Server accepts all requests carrying the MAC Address of the legitimate IoT client.
- All events are logged to 'Vulnerable_system.log'
- No signature or key verification is done hence confirms authentication system's vulnerability.

### Vulnerability of the system
Any attacker who discovers the MAC Address of the legitimate client can send forged requests and receive an 'ACCEPTED' response. This will be demostrated in .

## Part 2- Impersonation Attack Simulation

### Overview
This part demonstrates a successful impersonation attack against the
vulnerable server. The attacker uses Nmap to discover
the legitimate device's MAC address, then sends forged HTTP requests
using that address. Since the server only checks the MAC header, it
accepts all forged requests.

## Setup

### Kali 2 VM (Attacker)
1. Install dependencies: 'pip3 install requests'
2. Ensure Nmap is installed: 'sudo apt install nmap'

## Attack Steps

### Step 1 — Reconnaissance
```bash
sudo python3 Nmap_discovery.py
```
Note the MAC address of Kali 1 (the legitimate IoT device).

### Step 2 — Run the attack
1. Edit 'Attacker_device.py' — set 'server_url' and paste the discovered 'spoofed_mac_address'
2. Make sure the vulnerable server is still running on Ubuntu
```bash
python3 Attacker_device.py
```
## Expected Result
- All 10 forged requests accepted by the server
- Attack success rate: ~100%
- Results saved to 'Attacker.log'
- Server log on Ubuntu will also show 10 ACCEPTED entries from the attacker

## Evidence for Report
- Screenshot of attacker terminal showing SUCCESS on all attempts
- 'Attacker.log' from Kali 2
- 'Vulnerable_system.log' from Ubuntu Server showing no distinction between legitimate and forged requests