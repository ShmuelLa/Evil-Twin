#!/bin/sh
# sudo systemctl stop NetworkManager
# sudo airmon-ng check kill

# sudo ifconfig wlan1 down
# sudo iwconfig wlan1 mode monitor
# sudo ifconfig wlan1 up

sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

sudo ifconfig wlan1 up 10.100.101.1 netmask 255.255.255.0
sudo route add -net 10.100.101.0 netmask 255.255.255.0 gw 10.100.101.1
sudo ip link set wlan1 up

sudo iptables --table nat --append POSTROUTING --out-interface wlan0 -j MASQUERADE
sudo iptables --append FORWARD --in-interface wlan1 -j ACCEPT
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
sudo hostapd config/hostapd.conf