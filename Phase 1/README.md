# IoT-HMAC-Auth-System
HMAC-based IoT Authentication System
# Phase 1- Vulnerable IoT Server using Identifier-based Authentication 

## Overview
This phase demonstrates the vulnerability of MAC address-only authentication.
The Flask server accepts any HTTP request that presents a known MAC address
in the `mac-address` header, with no cryptographic verification

## Environment setup
### Ubuntu server VM
1. Install dependencies: 'pip3 install flask'
2. Run: 'python3 Vulnerable_server.py'
3. Server listens on port 5000

### Kali 1 VM- Legitimate IoT Client
1. Install dependencies: 'pip3 install requests'
2. Configure 'IoT_device.py' and set 'server_url' to the IP address if the Ubuntu Server.
3. Run: 'python3 IoT_device.py'

## Expected Behaviour
- Server accepts all requests carrying the MAC Address of the legitimate IoT client.
- All events are logged to 'Vulnerable_system.log'
- No signature or key verification is done hence confirms authentication system's vulnerability.

## Vulnerability of the system
Any attacker who discovers the MAC Address of the legitimate client can send forged requests and receive an 'ACCEPTED' response. This will be demostrated in Phase 2.
