import logging
from flask import Flask, request, jsonify

server=Flask(__name__)

logging.basicConfig(

    filename="Vulnerable_system.log", #The output of all log messages will be stored here.
    level=logging.INFO,             #It defines the messages that will be recorded in the system based on their severity level, level INFO and above. 
    format="%(asctime)s - %(levelname)s - %(message)s" #Controls how log messages will be formatted. It includes the timestamp, the severity level of the message, and the actual log message.
)

Registry={      
    "98:76:54:32:10:FE:DC:BA": "Temperature Sensor" #This registry is the dictionary that contains the MAC addresses and their corresponding client names.
}

@server.route("/data", methods=["POST"]) #POST method used by client to send data to the server. 
def receive_data():

    data_packet = request.get_json() #request.get_json() is used to convert the client's incoming JSON data into a Python dictionary.
    mac_address = request.headers.get("mac-address") #This line retrieves the value of the "mac-address" header from the incoming request.
    

    if not mac_address:
        print("No MAC address provided. Access denied!!")

        logging.warning("Access attempt without providing a MAC address.")

        return jsonify({
            "status": "No MAC address provided. Access denied!!"
            }), 400 #This line sends a JSON response back to the client, indicating that access is denied due to the absence of a MAC address. The status code 400 indicates a bad request.

    if mac_address in Registry: #This line checks if the retrieved MAC address exists in the Registry dictionary, which is used for authentication.
        name = Registry[mac_address] #If the MAC address is found in the registry, it retrieves the corresponding client name associated with that MAC address.
        
        temperature = data_packet.get("temperature") #This line retrieves the value of the "temperature" key from the data packet sent by the client.
        MAC = request.headers.get("mac-address") #This line retrieves the value of the "mac-address" header from the incoming request.
        print(f"Received data: {temperature}°C")
        print(f"MAC Address: {MAC}")

        logging.info("Authentication process initiated.")
        logging.info(f"{name} using MAC: {mac_address} requesting access to the server.")
        logging.info("Authentication started...")
        logging.info("Authentication process completed successfully.")
        logging.info(f"Authentication successful for {name} with MAC: {mac_address}. Data accepted :)")
        logging.info("System returned to waiting state...")

        return jsonify({
            "status": f"Welcome, {name}!.\n Data received successfully."
        }), 200 #This line sends a JSON response back to the client, indicating that the data was received successfully.
    
    else: 
        print("Unrecognized MAC address. Data rejected!!")

        logging.warning(f"Unauthorized access attempt using MAC: {mac_address}. Data rejected!!")
        logging.info("System returned to waiting state...")
        return jsonify({
            "status": "Data rejected.\n Unrecognized MAC address!!"
        }), 401
     #This line sends a JSON response back to the client, indicating that the data was rejected due to an unrecognized MAC address.


if __name__ == '__main__':
    print("=" * 50)
    print("\t\tVULNERABLE PHASE")
    print("=" * 50)
    print("[*] Server running on port 5000") 
    print("[*] Authentication method: MAC address only")
    server.run(
        host="127.0.0.1", 
        port=5000,
        debug=True) #This line starts the Flask server, making it accessible on to all the devices in the network
