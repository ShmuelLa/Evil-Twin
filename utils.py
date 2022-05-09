from rich.console import Console
from prompt_toolkit import prompt
import subprocess
import os

console = Console()

def main_menu_io():
    console.print('[bold]Please choose the desired option [blue]number[/]: \n\
    1. Set network interface \n\
    2. Start network scan \n\
    0. Exit program[/]\n')
    user_input = prompt('>> ')
    return user_input


def inet_set_menu():
    os.system('clear')
    console.print('[bold]Please inser the exact desired network interface [blue]name[/]: \n\
[red]Note: Interface must be set to Monitor mode[/] if it\'s not we will set it for you :wink: terface \n')
    os.system('iwconfig')
    net_interface = prompt('>> ')
    return net_interface


def set_inet_to_monitor(inet_name):
    try:
        subprocess.run(f'ifconfig {inet_name} down', check = True)
        subprocess.run(f'iwconfig {inet_name} mode monitor', check = True)
        subprocess.run(f'ifconfig {inet_name} up', check = True)
    except subprocess.CalledProcessError as e:
        console.print('[bold][red]Error while trying to set network interface to monitor more[/][/]')
        console.print(e.output)
    else:
        console.print('[bold][green]Network interface was successfuly set to monitor mode[/][/]')


def config_rouge_ap(ssid, inet, channel):
    """
    Creates a configuration file for the rouge access point with the next settings
    will be used with the hostapd command:
    https://wiki.gentoo.org/wiki/Hostapd

        **interface = The network interface we will use for this connection (the one that was
        previously set to monitor mode and used to the attack)
        **driver =  Nl80211 is a public 802.11 network driver docs:
        https://wireless.wiki.kernel.org/en/developers/documentation/nl80211
        **ssid = The network name
        **hw_mode = (Hardware Mode) Sets the 802.11 protocol to be used, doc about the various protocols 
        (we will set is to g): https://en.wikipedia.org/wiki/IEEE_802.11#Protocol
        **channel = Sets the channel for hostapd to work. (From 1 to 13)
        **macaddr_acl = Mac address filter (0 - off, 1 - on)
        **ign_broadcast_ssid = Sets hiddes AP mode on/off
        **auth_algs = Sets the authentication algorithm (0 - open, 1 - shared)
        **wpa = wpa version
        **wpa_passphrase = Sets wireless password
    """
    with open('config/ap.config', 'w') as f:
        f.write(f'interface={inet}\n')
        f.write('driver=nl80211\n')
        f.write(f'ssid={ssid}\n')
        f.write('hw_mode=g\n')
        f.write(f'channel={channel}\n')
        # f.write('macaddr_acl=0')
        # f.write('ignore_broadcast_ssid=0')
        # f.write('auth_algs=1')
        # f.write('wpa=2')
        # f.write('wpa_passphrase=shooshool')
        #  wpa_key_mgmt=WPA-PSK
        #  wpa_pairwise=CCMP
        #  wpa_group_rekey=86400
        #  ieee80211n=1
        #  wme_enabled=1
