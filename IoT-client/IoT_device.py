import requests
import json
import time
import random 

Device_id = "Temperature_Sensor"
Device_mac_address = 'mac address'
server_url= "server url"

def send_data():
    temperature_data= round(random.uniform(20.0, 40.0), 2)

    headers={
        "mac-address": Device_mac_address, 
        "device-id": Device_id, 
        "content-type": 'application/json' 
    }
    data_packet={
        "temperature": temperature_data,
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
    print(f"[*]\t\t IOT DEVICE STARTING UP")
    print("=" * 60)
    print(f"| MAC: {Device_mac_address} | Device ID: {Device_id}") 
    print("=" * 60)
for i in range(7):   
    send_data()
    time.sleep(2)