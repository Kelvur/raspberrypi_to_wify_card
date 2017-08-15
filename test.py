#!/usr/bin/python3

import unittest
import subprocess
from shutil import copy2
from os.path import exists

import setup

TEST_EXTENSION='.test'

def get_test_path(path):
	return path + TEST_EXTENSION

def begin_test(path):
	copy2(path, get_test_path(path))

def end_test(path):
	subprocess.check_call(['rm', get_test_path(path)])

#def compare_files(path, other_path):


class GeneralMethodsTestCase(unittest.TestCase):

	"""	SET UP	"""

	def setUp(self):
		self.path = globals()['__file__']
		self.wrong_path = self.path + '.cthulu_was_here'
		self.test_path = get_test_path(self.path)
		begin_test(self.path)

	def setUp_test_recover_backup_file(self):
		with open(self.test_path, 'a') as file:
			print('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac ex odio.', file=file)

	"""	TEST	"""

	def test_check_if_exists_return_none(self):
		self.assertIsNone(setup.check_if_exists(self.path))

	def test_check_if_exists_raise_error(self):
		self.assertRaises(IOError, setup.check_if_exists, self.wrong_path)

	def test_get_backup_path(self):
		self.assertEqual(self.path + setup.BACKUP_EXTENSION, setup.get_backup_path(self.path))

	def test_make_backup_file(self):
		setup.make_backup_file(self.test_path)
		self.assertTrue(exists(setup.get_backup_path(self.test_path)))

	def test_recover_backup_file(self):
		self.setUp_test_recover_backup_file()
		setup.recover_backup_file(self.test_path)
		#self.assertTrue(compare_files(self.test_path, setup.get_backup_file(self.test_path)))
		self.tearDown_test_recover_backup_file()

	def test_recover_backup_file_fail(self):
		self.assertRaises(IOError, setup.recover_backup_file, self.wrong_path)

	"""	TEAR DOWN	"""

	def tearDown_test_recover_backup_file(self):
		subprocess.check_call(['rm', setup.get_backup_path(self.test_path)])

	def tearDown(self):
		end_test(self.path)


if __name__ == '__main__':
	unittest.main(argv=[globals()['__file__'], '-v'])

