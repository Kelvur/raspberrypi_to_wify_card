#!/usr/bin/python3

import shutil
import subprocess
import argparse
import os.path
import re

class BasicConfigurationModel:
	
	BACKUP_EXTENSION = '.backup'
	TEST_EXTENSION = '.test'

	path = ''
	backup_path = ''
	test_path = ''
	settings = {}

	def __init__(self, backup=True):
		self.backup_path = self.get_backup_path(self.path)
		self.test_path = self.get_test_path(self.path)
		self.settings['backup'] = backup

	@staticmethod
	def get_backup_path(path):
		return path + BasicConfigurationModel.BACKUP_EXTENSION

	@staticmethod
	def get_test_path(path):
		return path + BasicConfigurationModel.TEST_EXTENSION

	@staticmethod
	def exists(path):
		return os.path.exists(path)
	
	@staticmethod
	def copy(origin, destiny):
		try:
			shutil.copy2(origin, destiny)
		except Error:
			return False
		return True

	@staticmethod
	def remove(path):
		try:
			subprocess.check_call(['rm', path])
		except CalledProcessError:
			return False
		return True

	@staticmethod
	def replace_in_file(path, old_string, new_string):
		replace = False
		buffer = ''
		with open(path, mode='r') as file:
			for line in file:
				if line == oldstring:
					buffer += new_string
					replaced = True
				else:
					buffer += line
		with open(path, mode='w') as file:
			print(buffer, file=file)
		return replace

	@staticmethod
	def read_file(path):
		buffer = ''
		with open(path, mode='r') as file:
			for line in file:
				buffer += line
		return buffer

	@staticmethod
	def write_file(path, buffer):
		with open(path, mode='w') as file:
			print(buffer, file=file)

	def configure(self):
		if self.settings['backup']:
			self.backup()
		if self._configure() == False:
			if self.settings['backup']:
				self.restore_backup()

	def _configure(self):
		return False

	def backup(self):
		return self.copy(self.path, self.backup_path)

	def remove_backup(self):
		self.remove(self.backup_path)

	def restore_backup(self):
		return self.copy(self.backup_path, self.path)	


class ConfigurationNetworkInterfaces(BasicConfigurationModel):
	
	path = '/home/pi/test/test.py'
	ETH0_INTERFACE = 'iface eth0 inet static\n\taddress 172.24.1.1\n\tnetmask 255.255.255.0\n\tnetwork 172.24.1.0\n\tbroadcast 172.24.1.255\n'
	ETH0_REGEX = r'^iface eth0 inet (manual)|(static(\n\t[\w\.\-/])+)'

	def __init__(self):
		BasicConfigurationModel.__init__(self)
	
	def _configure(self):
		buffer = self.read_file(self.path)
		result = re.subn(self.ETH0_REGEX, self.ETH0_INTERFACE, buffer, flags=re.MULTILINE)
		if result[1] == 0:
			return False
		self.write_file(self.path, result[0])
		return True

conf = ConfigurationNetworkInterfaces()
conf.configure()
