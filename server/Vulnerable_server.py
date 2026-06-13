import logging
from flask import Flask, request, jsonify

server=Flask(__name__)

logging.basicConfig(

    filename="Vulnerable_system.log", 
    level=logging.INFO,             
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

Registry={      
    "IoT_device MAC address": "IoT Device Name" 
}

@server.route("/data", methods=["POST"])  
def receive_data():

    data_packet = request.get_json() 
    mac_address = request.headers.get("mac-address") 
    

    if not mac_address:
        print("No MAC address provided. Access denied!!")

        logging.warning("Access attempt without providing a MAC address.")

        return jsonify({ "status": "No MAC address provided. Access denied!!" }), 400 

    if mac_address in Registry: 
        name = Registry[mac_address] 
        
        temperature = data_packet.get("temperature") 
        MAC = request.headers.get("mac-address") 
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
        }), 200 
    
    else: 
        print("Unrecognized MAC address. Data rejected!!")

        logging.warning(f"Unauthorized access attempt using MAC: {mac_address}. Data rejected!!")
        logging.info("System returned to waiting state...")
        return jsonify({
            "status": "Data rejected.\n Unrecognized MAC address!!"
        }), 401


if __name__ == '__main__':
    print("=" * 50)
    print("\t\tVULNERABLE PHASE")
    print("=" * 50)
    print("[*] Server running on port 5000") 
    print("[*] Authentication method: MAC address only")
    server.run(
        host="server's IP Address", 
        port=5000,
        debug=True) 