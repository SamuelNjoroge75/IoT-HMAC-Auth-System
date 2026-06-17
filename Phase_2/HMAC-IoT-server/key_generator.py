import secrets
import json
import os

key_file="device_keys.json"

def generate_key():
    return secrets.token_hex(32) #generates a 32-bit random secret key

def register_device(mac_address, device_name):
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            registry = json.load(f)
    else: 
        registry = {}

    key=generate_key()

    registry[mac_address] = {
        "name" : device_name,
        "key" : key 
    }

    with open(key_file, "w") as f:
        json.dump(registry, f, indent=4)

    print(f"[*] Device registered: {device_name}")
    print(f"[*] MAC Address      : {mac_address}")
    print(f"[*] Generated Key    : {key}")
    print(f"[*] Saved to         : {key_file}")
    return key

if __name__=="__main__":
    register_device("device's MAC Address","device name")
