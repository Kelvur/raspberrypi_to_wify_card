#!/usr/bin/python3

import shutil
import subprocess
import argparse
import os.path

class BaseError(Exception):
	"""Base error class for this module"""
	pass

class BackupError(BaseError):
	""""""
	pass

class PermisionError(BaseError):
	""""""
	pass

class FileError(BaseError):
	""""""
	pass

class BasicConfigurationModel:
	
	BACKUP_EXTENSION = '.backup'
	TEST_EXTENSION = '.test'

	path = ''
	backup_path = ''
	test_path = ''

	def __init__(self, backup=true):
		backup_path = get_backup_path(path)
		test_path = get_test_path(path)
		configurate(self, path)

	@classmethod
	def get_backup_path(path):
		return path + BACKUP_EXTENSION

	@classmethod
	def get_test_path(path):
		return path + TEST_EXTENSION

	@classmethod
	def exists(path):
		return os.path.exists(path)

	def configurate(self, path):
		return

	#def copy(origin, destiny):

	def backup(self):
		shutil.copy2(self.path, self.backup_path)

	def restore_backup(self):
		if exists(self.backup_path):
			shutil.copy2(self.backup_path, self.path)
		else:
			raise FileError()
	
	def remove_backup(self):
		if exists(self.backup_path):
			break
