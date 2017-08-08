#!/usr/bin/python3

import argparse
import os.path
import shutil

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
BACKUP_EXTENSION = '.backup'

def print_file(path):
	with open(path, 'r') as file:
		for line in file:
			print(line, end='')
	file.close()

def make_file_backup(path):
	shutil.copy2(path, path + BACKUP_EXTENSION)

def replace_in_file(file, old_string, new_string)
	replaced = False
	for line in file:
		if(line == old_string)
			file.write(new_string)
			replaced = True
		else:
			file.write(line)
	return value
	
def configurate_network_interface():
	if path.exists(PATH_NET_INTERFACE)
		try:
			if !ARGS.no-backup:
				make_file_backup(PATH_NET_INTERFACES)
			file = open(PATH_NET_INTERFACES, mode='+')
			if !replace_in_file(file, 'iface eth0 inet manual', 'iface eth0 inet static\n\taddress 172.24.1.1\n\tnetmask 255.255.255.0\n\tnetwork 172.24.1.0\n\tbroadcst 172.24.1.255\n'):
				raise Error('The file {0} has been modificated before.'.format(PATH_NET_INTERFACES))
		except OSError as error:
			file.close()
			print('OS Error: {0}'.format(error))
	if !ARGS.no-backup:
		
