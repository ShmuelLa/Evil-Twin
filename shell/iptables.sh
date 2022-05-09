sudo iptables --table nat --append POSTROUTING --out-interface wlan0 -j MASQUERADE
sudo iptables --append FORWARD --in-interface wlan1 -j ACCEPT
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
#check if 1
sudo sysctl net.ipv4.ip_forward