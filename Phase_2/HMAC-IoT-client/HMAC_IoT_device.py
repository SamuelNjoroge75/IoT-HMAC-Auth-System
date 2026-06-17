import requests
import json
import time
import random 
import hmac
import hashlib

Device_id = "device name"
Device_mac_address = 'device mac address'
server_url= "http://server's IP Address:5000"
secret_key="device's secret key from 'key_generator.py'"

def compute_hmac(data_packet_str):
    return hmac.new(
        secret_key.encode(),
        data_packet_str.encode(),
        hashlib.sha256
    ).hexdigest()

def send_data():
    temperature_data= round(random.uniform(20.0, 40.0), 2) 

    data_packet={
        "temperature": temperature_data,
    } 

    packet_str=json.dumps(
        data_packet,
        separators=(',',':'),
        sort_keys=True
    )
    signature=compute_hmac(packet_str)

    headers={
        "mac-address": Device_mac_address, 
        "device-id": Device_id,  
        "hmac-signature": signature,
        "content-type": 'application/json' 
    }


    try: 
        response = requests.post(
            server_url + "/data",
            headers=headers,
            json=data_packet
        )
        print(f"Status Code: {response.status_code}")
        response_data= response.json()

        if response.status_code ==200:
            print(f"Data sent successfully: {temperature_data}°C") 
        else:
            print(f"Failed to send data.\nServer response: {response_data['status']}") 

    except Exception as e:
        print(f"An error occurred while sending data to the server: {e}") 


if __name__ == '__main__':
    print("=" * 60)
    print(f"[*]\t\t HMAC IOT DEVICE STARTING UP")
    print("=" * 60)
    print(f"[*] Authentication: HMAC-SHA256 enabled")
    print("=" * 60)
    print(f"| MAC: {Device_mac_address} | Device ID: {Device_id}") 
    print("=" * 60)
for i in range(7):
    send_data()
    time.sleep(2)
