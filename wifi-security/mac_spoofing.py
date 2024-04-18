import subprocess
import re

def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ip", "link", "show", interface]).decode('utf-8')
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print(f"Could not read MAC address from {interface}.")
            return None
    except subprocess.CalledProcessError:
        print(f"Failed to execute ip link for {interface}.")
        return None

def change_mac(interface, new_mac):
    print(f"Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "up"])

    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print(f"MAC address was successfully changed to {current_mac}")
    else:
        print("Failed to change MAC address.")

if __name__ == "__main__":
    interface = "enp0s8"  # Adjust to your interface
    new_mac = "44:91:60:EA:E3:DF"  # New MAC

    current_mac = get_current_mac(interface)
    print(f"Current MAC: {current_mac}")
    change_mac(interface, new_mac)
