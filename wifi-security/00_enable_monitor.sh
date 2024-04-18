#!/bin/bash
sudo ip link set wlx24050fe36984 down 
sudo iwconfig wlx24050fe36984 mode monitor 
sudo ip link set wlx24050fe36984 up
