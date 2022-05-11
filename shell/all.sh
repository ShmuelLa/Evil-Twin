#!/bin/sh
# sudo systemctl stop NetworkManager
# sudo airmon-ng check kill

# sudo ifconfig wlx5ca6e686a840 down
# sudo iwconfig wlx5ca6e686a840 mode monitor
# sudo ifconfig wlx5ca6e686a840 up

sudo ifconfig wlx5ca6e686a840 down
sudo iwconfig wlx5ca6e686a840 mode monitor
sudo ifconfig wlx5ca6e686a840 up

sudo ifconfig wlx5ca6e686a840 up 10.100.101.1 netmask 255.255.255.0
sudo route add -net 10.100.101.0 netmask 255.255.255.0 gw 10.100.101.1
sudo ip link set wlx5ca6e686a840 up

sudo iptables --table nat --append POSTROUTING --out-interface wlo1 -j MASQUERADE
sudo iptables --append FORWARD --in-interface wlx5ca6e686a840 -j ACCEPT
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
sudo hostapd config/hostapd.conf

#sudo dnsmasq -C config/dns.conf -d
