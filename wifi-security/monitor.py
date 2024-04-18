import subprocess

# Configuration parameters
mac_address = "44:91:60:EA:E3:DF"  # Replace with the target MAC address
interface = "wlx24050fe36984"  # Change to your interface name, e.g., "eth0" for Ethernet
capture_filter = f"ether src {mac_address} or ether dst {mac_address}"
output_file = "specific_mac_traffic.pcap"
number_of_packets = 100  # Number of packets to capture

# Construct the tshark command with interface specification
tshark_command = [
    "tshark",
    "-i", interface,  # Specify the network interface
    "-c", str(number_of_packets),  # Capture N packets
    "-f", capture_filter,  # Use the capture filter
    "-w", output_file,  # Write the output to a file
]

# Execute the command
try:
    print(f"Starting packet capture on {interface} for MAC address: {mac_address}")
    subprocess.run(tshark_command, check=True)
    print(f"Capture completed. Data saved to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred during packet capture: {e}")
