import subprocess # Allows us to run external commands (like Nmap) inside a Python script and capture its output.
import re #Used to help extract the MAC Addresses from the Nmap output.
import sys #Used to handle command-line arguments and exit the script gracefully if needed.


Target_subnet = "subnet" #This is the local network we want to scan for devices.

def discover_mac_addresses():
    print("[*] Starting network discovery using Nmap...")

    try:
        # Run Nmap to discover devices on the local network
        result = subprocess.run(
            ['nmap', '-sn', "--privileged",Target_subnet], #This command runs Nmap in "ping scan" mode (-sn) to discover active hosts on the specified subnet. The --privileged flag allows Nmap to perform certain operations that may require elevated permissions.
            capture_output=True, 
            text=True,
            timeout=5
        )
        output = result.stdout #This captures the standard output of the Nmap command, which contains the results of the scan. 
        print(output) #This prints the raw output from Nmap to the console, allowing us to see the results of the scan directly.


        # Extract MAC addresses from the Nmap output
        devices=[] #This initializes an empty list to store the discovered devices (MAC addresses).
        current_ip = None #This variable is used to keep track of the current IP address being processed in the Nmap output. It helps associate discovered MAC addresses with their corresponding IP addresses.

        for line in output.splitlines(): #This loop iterates through each line of the Nmap output, allowing us to process the results line by line.
            ip_match = re.search(r'Nmap scan report for ([\d\.]+)', line) #This regular expression searches for lines that indicate a new host has been discovered, capturing the IP address of that host.
            mac_match = re.search(r'MAC Address: ([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', line) #This regular expression searches for lines that contain a MAC address, capturing the MAC address in the process.

            if ip_match:
                current_ip = ip_match.group(1) #If a new host is found, we update the current_ip variable with the captured IP address.

            if mac_match and current_ip: #If a MAC address is found and we have a current IP address, we associate the MAC address with that IP and add it to our list of devices.
                mac_address = mac_match.group(1)
                devices.append((current_ip, mac_address))
                print(f"Discovered device: IP={current_ip}, MAC={mac_address}") #This prints out the discovered device's IP and MAC address.
    
        if not devices:
            print("No devices found on the network. Make sure you're on the same subnet!!")
        else:
            print(f"Total devices discovered: {len(devices)}")
    
    except subprocess.SubprocessError as e:
        print(f"Error occurred while running Nmap: {e}")
        sys.exit(1) #If there is an error running the Nmap command, we print an error message and exit the script with a non-zero status code to indicate failure.    

if __name__ == "__main__":
    print("[*] Attacker phase: Network Reconnaissance using Nmap.")
    print("=" * 50) #This prints a separator line for better readability in the console output.)
    discover_mac_addresses()
    