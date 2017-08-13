#!/usr/bin/python3

import argparse
import os.path
import shutil
import subprocess

def parse_args():
	parser = argparse.ArgumentParser("Configurate your Raspberry Pi to set it like a ethernet access point.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', help="Display more info while the execution.", action='store_true')
	group.add_argument('-q', '--quiet', help="No display any info while the execution.", action='store_true')
	parser.add_argument('--no-backup', help="By default the script make backups of the files it will modificate, if you do not want this behaviour use this argument.", action='store_true')
	return parser.parse_args()

ARGS = parse_args()
PATH_NET_INTERFACES = '/etc/network/interfaces'
PATH_DHCPCD_CONF = '/etc/dhcpcd.conf'
PATH_DNSMASQ_CONF = '/etc/dnsmasp.conf'
PATH_SYSCTL_CONF = '/etc/sys.ctl.conf'
PATH_IPTABLES = '/etc/iptables.ipv4.nat'
PATH_IPTABLES_BACKUP = '/etc/iptables.ipv4.backup'
PATH_RCLOCAL = '/etc/rc.local'
BACKUP_EXTENSION = '.backup'

def check_if_exists(path):
	if os.path.exists(path) == False:
		raise IOError('The file {0} does not exists.'.format(path))

def get_backup_path(path):
	return path + BACKUP_EXTENSION

def make_file_backup(path):
	shutil.copy2(path, get_backup_path(path))

def recover_file_backup(path):
	path_backup = get_backup_path(path)
	if os.path.exists(path_backup) == False:
		raise IOError('Cannot recover {0} to the original state, {1} does not exists.'.format(path, path_backup))
	shutil.copy2(path_backup, path)

def replace_in_file(file_name, old_string, new_string):
	replaced = False
	buffer = ''
	with open(file_name, mode='r') as file:
		for line in file:
			if(line == old_string):
				buffer += new_string
				replaced = True
			else:
				buffer += line
	with open(file_name, mode='w') as file:
		print(buffer, file=file)
	return replaced
	
def configurate_network_interfaces():
	check_if_exists(PATH_NET_INTERFACES)
	if ARGS.no_backup == False:
		backup_network_interfaces()
	if replace_in_file(PATH_NET_INTERFACES, 'iface eth0 inet manual\n', 'iface eth0 inet static\n\taddress 172.24.1.1\n\tnetmask 255.255.255.0\n\tnetwork 172.24.1.0\n\tbroadcast 172.24.1.255\n') == False:
		raise IOError('The file {0} was modificated before.'.format(PATH_NET_INTERFACES))


def backup_network_interfaces():
	make_file_backup(PATH_NET_INTERFACES)
	
def recover_network_interfaces():
	recover_file_backup(PATH_NET_INTERFACES)

def configurate_dhcpcd():
	check_if_exists(PATH_DHCPCD_CONF)
	if ARGS.no_backup == False:
		backup_dhcpcd()
	with open(PATH_DHCPCD_CONF, mode='a') as file:
		print('\ndenyinterfaces eth0', file=file)

def backup_dhcpcd():
	make_file_backup(PATH_DHCPCD_CONF)

def restore_dhcpcd():
	recover_file_backup(PATH_DHCPCD_CONF)
		
def install_dnsmasq():
	subprocess.run(['apt-get', 'install', 'dnsmasq', '--yes'], check=True)

def configurate_dnsmasq():
	check_if_exists(PATH_DNSMASQ_CONF)
	if ARGS.no_backup == False:
		backup_dnsmasq()
	with open(PATH_DNSMASQ_CONF, mode='a') as file:
		print('\ninterface=eth0\nlisten_address=172.24.1.1\nbind-interfaces\nserver=8.8.8.8\domain-needed\nbogus-priv\ndhcp-range=172.24.1.50,172.24.1.150,12h\n', file=file)

def backup_dnsmasq():
	make_file_backup(PATH_DNSMASQ_CONF)

def restore_dhcpmasq():
	recover_file_backup(PATH_DNSMASQ_CONF)

def configurate_sysctl():
	check_if_exists(PATH_SYSCTL_CONF)
	if ARGS.no_backup == False:
		backup_sysctl()
	if replace_in_file(PATH_SYSCTL_CONF, '#net.ipv4.ip_forward=1\n', 'net.ipv4.ip_forward=1') == False:
		raise IOError('The file {0} was modificated before.'.format(PATH_SYSTCL_CONF))

def backup_sysctl():
	make_file_backup(PATH_SYSCTL_CONF)

def restore_sysctl():
	recover_file_backup(PATH_SYSCTL_CONF)

def configurate_iptables():
	if ARGS.no_backup == False:
		backup_iptables()
	subprocess.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'wlan0', '-j', 'MASQUERADE'], check=True)
	subprocess.run(['iptables', '-A', 'FORWARD', '-i', 'wlan0', '-o', 'eth0', '-m', 'state', '--state', 'RELATED,ESTABLISHED', '-j', 'ACCEPT'], check=True)
	subprocess.run(['iptables', '-A', 'FORWARD', '-i', 'eth0', '-o', 'wlan0', '-j', 'ACCEPT'], check=True)
	#Save configuration
	subprocess.run(['iptables-save', '>', PATH_IPTABLES_CONF], check=True)

def backup_iptables():
	subprocess.run(['iptables-save', '>', PATH_IPTABLES_BACKUP], check=True)

def restore_iptables():
	subprocess.run(['iptables-restore', '<', PATH_IPTABLES_BACKUP], check=True)


# CONFIGURATE NETWORK INTERFACES

# CONFIGURATE DHCPCD

# INSTALL DNSMASQ

# CONFIGURATE DNSMASQ

# CONFIGURATE SYSCTL

# SET IPTABLES

# CHECK IF SERVICES AND INTERFACES ARE UP
