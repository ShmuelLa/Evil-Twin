from scapy.all import *
import multiprocessing
import time
import os
from scapy.layers.dot11 import Dot11Beacon, Dot11Elt, Dot11, Dot11ProbeResp

"""
Use:
Run main (or wrap in another function), enter interface to fit your card.
wait until scan if complete and choose a network
returns a tuple of (mac address,ap name,channel, and signal dbm)
"""

def sniffAP(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        mac_addr = packet[Dot11].addr2
        # get the name of it
        ap_name = packet[Dot11Elt].info.decode()
        # get dbm signal
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats for channel
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        if mac_addr not in network_dict.keys():
            network_dict[mac_addr] = (mac_addr,ap_name, channel, dbm_signal)


# changing channel every 2 seconds, for timeout times.
def changeChannel(timeout: int):
    channel = 1
    counter = 0
    while True:
        # os command to switch channels.
        os.system(f"iwconfig {interface} channel {channel}")
        channel = channel % 14 + 1
        time.sleep(2)
        print(f"scanning channel: {channel}")
        counter += 1
        if counter == timeout:
            break


# called after scan was finished, allows user to choose network by index of display, or mac address.
def pickNetwork():
    mac_ok = False
    while not mac_ok:
        network_mac = input("Please enter a valid index or MAC address of the network you want to attack: ")
        if len(network_mac) < 16:  # shorter than mac address TODO: this can be problematic in case we have a lot of networks scanned.
            if int(network_mac) not in network_index.keys():
                print("ERROR, not a valid index")
                continue
            else:
                print("Valid index")
                network = network_dict.get(network_index.get(int(network_mac)))
                print(f"Chosen network: {network}")
                return network
        if network_mac not in network_dict.keys():
            print("ERROR, not a valid MAC address")
            continue
        if network_mac in network_dict.keys():
            print(f"Chosen network: {network_dict.get(network_mac)}")
            mac_ok = True
    return network_dict.get(network_mac)


if __name__ == "__main__":
    global network_dict
    network_dict = {}  # holds network stats - mac,name,channel
    network_index = {}  # for easy access to network using index

    # if no timeout is passed, default to 60 seconds
    if len(sys.argv) > 1:
        timeout = int(sys.argv[1])
    else:
        timeout = 60

    # interface name
    interface = "wlx5ca6e686a840"
    # start the thread that changes channels all the networks
    channel_changer = multiprocessing.Process(target=changeChannel(timeout))
    channel_changer.start()
    sniff(prn=sniffAP, iface=interface, timeout=timeout)

    # Create network index dict, and prompt picking of a network.
    i = 0
    print("Available networks:")
    for network in network_dict.keys():
        network_addr = network_dict.get(network)[0]
        network_name = network_dict.get(network)[1]
        channel = network_dict.get(network)[2]
        dbm = network_dict.get(network)[3]
        print(f"MAC: {network_addr} | NAME: {network_name} | CHANNEL: {channel} | SIGNAL DBM: {dbm}")
        network_index[i] = network
        i += 1
    pickNetwork()