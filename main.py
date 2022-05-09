from numpy import size
import os
from scapy.all import get_if_list
from prompt_toolkit import prompt
from rich.console import Console
import click
from utils import *
from pyfiglet import figlet_format
from termcolor import cprint

os.system('clear')
console = Console()
cprint(figlet_format('Welcome to the EvilTwin Framework!', font='slant'), 'green', attrs=['bold'])
net_interface = None

while 1:
    user_input = main_menu_io()
    if user_input == "0":
        os.system('clear')
        cprint(figlet_format('Goodbye!', font='slant'), 'green')
        exit()
    elif user_input == "1":
        net_interface = inet_set_menu()
        while net_interface not in get_if_list() or net_interface is None:
            net_interface = prompt(f'Please insert correct interface name from the next list: [{" ".join(get_if_list())}] \n>> ')
        set_inet_to_monitor(net_interface)


