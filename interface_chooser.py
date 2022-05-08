from scapy.all import *
import netifaces
import os

if_dict = {}

# for iface in get_if_list():
#     print(netifaces.ifaddresses(iface))

os.system('iwconfig')