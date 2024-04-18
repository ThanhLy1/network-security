#!/bin/bash

# Bring the interface down
sudo ifconfig wlx24050fe36984 down

# Set the interface to monitor mode
sudo iwconfig wlx24050fe36984 mode monitor

# Bring the interface up
sudo ifconfig wlx24050fe36984 up

# Define the MAC address you want to capture packets from/to
TARGET_MAC="B8-31-B5-88-36-7C"

# Define the output file
OUTPUT_FILE="captured_packets.pcap"

# Start capturing packets
echo "Starting packet capture for MAC $TARGET_MAC..."
sudo tcpdump -i wlx24050fe36984 -U -w $OUTPUT_FILE ether host $TARGET_MAC

# Note: Press Ctrl+C to stop the capture
