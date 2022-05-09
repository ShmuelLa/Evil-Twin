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
