import logging
import hmac
import hashlib
import json
import os
from flask import Flask, request, jsonify

server=Flask(__name__)

logging.basicConfig(
    filename="HMAC_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

key_file="device_keys.json"

def load_registry():
        if os.path.exists(key_file):
            with open(key_file, "r") as f:
                return json.load(f)
        else:
             print(f"[ERROR] {key_file} not found. Run generate_keys.py first.")
        return {}

Registry= load_registry()

def get_secret_key(mac_address):
    device = Registry.get(mac_address)
    if device:
        return device["key"]
    return None

def verify_hmac(
        mac_address,
        packet_str,
        received_signature
    ):
    device=Registry.get(mac_address)
    if not device:
        return False

    secret_key=device["key"]
    expected_signature=hmac.new(
        secret_key.encode(),
        packet_str.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        received_signature
    )

@server.route("/data", methods=["POST"]) 
def receive_data():

    data_packet = request.get_json()
    mac_address = request.headers.get("mac-address")
    received_signature= request.headers.get("hmac-signature")

    name = Registry[mac_address]["name"]

    logging.info("Authentication process initiated.")
    logging.info(f"{name} using MAC: {mac_address} requesting access to the server.")
    logging.info("Authentication started...")

    if not mac_address:
        print("No MAC address provided. Access denied!!")
        logging.warning("Access attempt without providing a MAC address.")

        return jsonify({
            "status": "No MAC address provided. Access denied!!"
            }), 400

    if mac_address not in Registry:
        print("Unrecognized MAC Address. Data rejected!!")
        logging.warning(f"Unauthorized access attempt using invalid MAC {mac_address}. Data rejected!!")
        logging.info("System returned to waiting state...")
        return jsonify({
            "status": "Data rejected.\nUnrecognised MAC Address!!"
        }), 401
    else:
        print("[*] MAC Address valid. Checking device's signature...")
        logging.info(f"[*] Valid MAC address from {name}. Checking device's signature...")

    if not received_signature:
        print(f"[ALERT!!] Missing HMAC signature from MAC: {mac_address}")
        logging.warning(f"ALERT: Missing HMAC signature | MAC {mac_address} | POSSIBLE IMPERSONATION ATTACK!!")
        return jsonify({
            "status": "Data rejected.\nMissing HMAC signature!!"
        }), 401
    else:
        print(f"Valid HMAC signature from MAC: {mac_address}. Verifying signature...")
        logging.info(f"[*] Valid HMAC signature from MAC: {mac_address}. Verifying device's signature...")

    packet_str= json.dumps(
        data_packet,
        separators=(',',':'), 
        sort_keys=True
    )
     
    if not verify_hmac( mac_address, packet_str, received_signature ):
        print(f"[ALERT!!] Signatures Mismatch!! Invalid HMAC signature from MAC: {mac_address}")
        logging.warning(f"ALERT!!: Signatures Mismatch!! Invalid HMAC signature | MAC: {mac_address}. POSSIBLE IMPERSONATION ATTACK!!")
        return jsonify({
            "status": "Data rejected.\n Invalid HMAC Signature!!"
        }), 401
    else:
        print(f"[*]Signatures Match. Verification successful.\nData accepted :)")
        logging.info(f"[*]Signatures Match. Signature Verification successful.")

    temperature = data_packet.get("temperature") 
    mac_address = request.headers.get("mac-address") 
    print(f"Received data: {temperature}°C")
    print(f"MAC Address: {mac_address}")

    logging.info("Authentication process completed successfully.")
    logging.info(f"Authentication successful for {name} with MAC: {mac_address}. Data accepted :)")
    logging.info("System returned to waiting state...")

    return jsonify({
        "status": f"Welcome, {name}!.\n Data received successfully."
    }), 200
    

if __name__ == '__main__':
    print("=" * 50)
    print("\t\tHMAC-SECURED PHASE")
    print("=" * 50)
    print("[*] Server running on port 5000") 
    print("[*] Authentication method: HMAC Verification.")
    server.run(
        host="server's IP Address", 
        port=5000,
        debug=True)
