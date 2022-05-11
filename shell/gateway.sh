#!/bin/sh
# sudo ip link set wlan1 down
sudo ifconfig wlx5ca6e686a840 up 10.100.101.1 netmask 255.255.255.0
sudo route add -net 10.100.101.0 netmask 255.255.255.0 gw 10.100.101.1
sudo ip link set wlx5ca6e686a840 up
