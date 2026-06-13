import requests
import json
import time
import random 

Device_id = "Temperature_Sensor"
Device_mac_address = '98:76:54:32:10:FE:DC:BA'
server_url= "http://127.0.0.1:5000"

def send_data():
    temperature_data= round(random.uniform(20.0, 40.0), 2) #This generates a random temperature value between 20.0 and 40.0 degrees Celsius, rounded to 2 decimal places.

    headers={
        "mac-address": Device_mac_address, #This header authenticates the device by providing its MAC address.
        "device-id": Device_id, #This header is used to identify the type of device that is sending the request. 
        "content-type": 'application/json' #specifies that the data being sent is in JSON format.
    }
    data_packet={
        "temperature": temperature_data,
    } #This is the actual data being sent by the device. 

    try: #This block is used to handle any exceptions that may occur during the process of sending data to the server. If an error occurs, it will be caught and an error message will be printed.
        response = requests.post(
            server_url + "/data",
            headers=headers,
            json=data_packet
        ) #This line sends a POST request to the server at the specified URL with the defined headers and JSON data.
                #The server will process this request and return a response based on the authentication of the device.
        print(f"Status Code: {response.status_code}")
        response_data= response.json()

        if response.status_code ==200:
            print(f"Data sent successfully: {temperature_data}°C") #Information being sent to server.
        else:
            print(f"Failed to send data.\nServer response: {response_data['status']}") 
        

    except Exception as e:
        print(f"An error occurred while sending data to the server: {e}") # Prints a readable error message if there is an issue with sending data to the server. 


if __name__ == '__main__':
    print("=" * 60)
    print(f"[*]\t\t IOT DEVICE STARTING UP")
    print("=" * 60)
    print(f"| MAC: {Device_mac_address} | Device ID: {Device_id}") #It runs the send_data function in a loop, sending data to the server every 2 seconds for a total of 7 readings.
    print("=" * 60)
for i in range(7):   # Sends 7 temperature readings
    send_data()
    time.sleep(2)