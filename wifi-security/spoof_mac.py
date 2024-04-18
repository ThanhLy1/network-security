import subprocess
import sys

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 spoof_mac.py <interface> <new_mac>")
        sys.exit(1)

    interface = sys.argv[1]
    new_mac = sys.argv[2]

    change_mac(interface, new_mac)
    print(f"[+] MAC address was changed to {new_mac}")
