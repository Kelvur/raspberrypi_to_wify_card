#!/usr/bin/python3

import shutil
import setup

TEST_EXTENSION='.test'
def get_test_path(path):
	return path + TEST_EXTENSION

def begin_test(path):
	shutil.copy2(path, get_test_path(path))

def end_test(path):
	subprocess.run(['rm', get_test_path(path)], check=True)


