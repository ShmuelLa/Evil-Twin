from scapy.all import *

iface = "wlan1"
sender_mac = RandMAC()
ssid = "AfikKhmar"
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)

# beacon layer
beacon = Dot11Beacon()
# putting ssid in the frame
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
frame = RadioTap()/dot11/beacon/essid

sendp(frame, inter=0.1, iface=iface, loop=1)