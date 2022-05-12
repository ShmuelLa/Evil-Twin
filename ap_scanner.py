from scapy.all import *
import multiprocessing
import time
import os
from scapy.layers.dot11 import Dot11Beacon, Dot11Elt, Dot11

"""
Use:
Run main (or wrap in another function), enter interface to fit your card.
wait until scan if complete and choose a network
returns a tuple of (mac address,ap name,channel, and signal dbm)
"""

global network_dict
network_dict = {}  # holds network stats - mac,name,channel
network_index = {}  # for easy access to network using index
my_macs = [] #= [get_if_hwaddr(i) for i in get_if_list()] # so we don't attack ourselves
client_dict = {}
client_index = {}


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
        if mac_addr not in network_dict.keys()and mac_addr not in my_macs:
            network_dict[mac_addr] = (mac_addr, ap_name, channel, dbm_signal)
            print(f"Found AP:{network_dict[mac_addr]}")


# changing channel every 2 seconds, for timeout times.
def changeChannel(timeout: int, interface):
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
        network_mac = input("Please enter an index (starting from 0) or MAC address of the network you want to attack: ")
        if not any(c.isalpha() for c in str(network_mac)): #if index is entered there will be no letters
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
            return network_dict.get(network_mac)


def scanClients(target_ap):
    def packet_handler(packet):
        if (packet.addr2 == target_ap or packet.addr3 == target_ap) and packet.addr1 != 'ff:ff:ff:ff':
            if packet.addr1 not in client_dict[target_ap].keys() and packet.addr2!=packet.addr1 and packet.addr1!=packet.addr3:
                client_dict[target_ap][packet.addr1] = (packet.addr1, packet.addr2)
                print(f"Found a possible client: MAC: {client_dict[target_ap][packet.addr1][0]} | Name: {client_dict[target_ap][packet.addr1][1]}")


def pickClient(target_ap):
    client_ok = False
    while not client_ok:
        client_mac = input("Please enter an index (starting from 0) or MAC address of the client you want to attack: ")
        if not any(c.isalpha() for c in str(client_mac)): #if index is entered there will be no letters
            if int(client_mac) not in client_dict[target_ap].keys():
                print("ERROR, not a valid index")
                continue
            else:
                print("Valid index")
                #equivelent to client_dict[target_ap].get(client_index[target_ap].get(int(client_mac)))[0]
                client_mac = client_index[target_ap].get(int(client_mac))
                print(f"MAC chosen: {client_mac}")
                return client_mac
        if client_mac not in client_dict[target_ap].keys():
            print("Error, not a valid MAC address")
            continue
        if client_mac in client_dict[target_ap].keys():
            #in ap client dict, get the mac address stored in tuple[0]
            client_mac = client_dict[target_ap].get(client_mac)[0]
            print(f"MAC chosen: {client_mac}")
            return client_mac
    return client_mac


def setMonitor(interface):
    os.system(f"sudo ifconfig {interface} down")
    os.system(f"sudo iwconfig {interface} mode monitor")
    os.system(f"sudo ifconfig {interface} up")


def ap_client_scanner(interface):
    """
    return: ((mac_addr, ap_name, channel, dbm_signal), chosen_client_mac)
    """
    # interface name
    setMonitor(interface)
    # if no timeout is passed, default to 60 seconds
    timeout = 30

    # ----------------------------PART 1: scan and pick network ---------------------
    # start the thread that changes channels all the networks

    channel_changer = multiprocessing.Process(target=changeChannel,args=(timeout,interface),daemon=True)
    channel_changer.start()
    sniff(prn=sniffAP,iface=interface, timeout=timeout)
    channel_changer.join()
    # Create network index dict, and prompt picking of a network.
    i = 0
    print("Available Networks:")
    for network in network_dict.keys():
        network_addr = network_dict.get(network)[0]
        network_name = network_dict.get(network)[1]
        channel = network_dict.get(network)[2]
        dbm = network_dict.get(network)[3]
        print(f"Index: {i} | MAC: {network_addr} | NAME: {network_name} | CHANNEL: {channel} | SIGNAL DBM: {dbm}")
        network_index[i] = network
        i += 1
    chosen_network = pickNetwork()
    chosen_network_mac = chosen_network[0]
    # --------------------------------------------------------------------------------------------------
    # ----------------------------PART 2: scan and pick client from chosen network ---------------------

    client_dict[chosen_network_mac] = {}  # define a dictionary for each ap inside a general dict
    channel_changer = multiprocessing.Process(target=changeChannel, args=(timeout,interface), daemon=True)
    channel_changer.start()
    sniff(iface = interface, prn=scanClients(chosen_network_mac), timeout=timeout)
    channel_changer.join()
    i = 0
    print("Possible Clients:")
    for client in client_dict[chosen_network_mac].keys():
        client_mac = client_dict[chosen_network_mac][client][0]
        print(f"MAC:{client_mac}")
        client_index[chosen_network_mac][i] = client_dict[chosen_network_mac][0]
        i += 1
    chosen_client_mac = pickClient(chosen_network_mac)
    return chosen_network, chosen_client_mac

    