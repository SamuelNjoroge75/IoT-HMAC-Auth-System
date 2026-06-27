import subprocess 
import re 
import sys 


Target_subnet = "subnet" 

def discover_mac_addresses():
    print("[*] Starting network discovery using Nmap...")

    try:
        # Run Nmap to discover devices on the local network
        result = subprocess.run(
            ['nmap', '-sn', "--privileged",Target_subnet], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        output = result.stdout 
        print(output) 

        # Extract MAC addresses from the Nmap output
        devices=[] 
        current_ip = None 

        for line in output.splitlines():
            ip_match = re.search(r'Nmap scan report for ([\d\.]+)', line) 
            mac_match = re.search(r'MAC Address: ([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})', line)

            if ip_match:
                current_ip = ip_match.group(1) 

            if mac_match and current_ip: 
                mac_address = mac_match.group(1).lower()
                devices.append((current_ip, mac_address))
                print(f"Discovered device: IP={current_ip}, MAC={mac_address}") 
    
        if not devices:
            print("No devices found on the network. Make sure you're on the same subnet!!")
        else:
            print(f"Total devices discovered: {len(devices)}")
    
    except subprocess.SubprocessError as e:
        print(f"Error occurred while running Nmap: {e}")
        sys.exit(1)     

if __name__ == "__main__":
    print("[*] Attacker phase: Network Reconnaissance using Nmap.")
    print("=" * 50) 
    discover_mac_addresses()
    