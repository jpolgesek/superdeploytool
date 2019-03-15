#coding: utf-8
import os
import errno
import shutil
import inspect

FATAL = 0
ERROR = 1
WARNING = 2
INFO = 3
VERBOSE = 4
DEBUG = 5

USE_COLORS = False
SHOW_LINES = True
SHOW_TIME = False
SHOW_LEVEL = False
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def log(text = "Default text", level = None):
	previous_frame = inspect.currentframe().f_back
	filename, line_number, _, __, ___ = inspect.getframeinfo(previous_frame)

	filename = os.path.basename(filename)

	#if filename[0] == ".":
	#	filename = filename[2:]
	
	if SHOW_LINES:
		output = "[{:>16}] {}".format(
			"{}:{}".format(filename, line_number),
			text
		)
	else:
		output = text

	if USE_COLORS:
		if level == FATAL:
			output = bcolors.UNDERLINE + bcolors.FAIL + output + bcolors.ENDC

		elif level == ERROR:
			output = bcolors.FAIL + output + bcolors.ENDC
		
		elif level == WARNING:
			output = bcolors.WARNING + output + bcolors.ENDC
		
		elif level == INFO:
			pass
			#output = bcolors.OKGREEN + output + bcolors.ENDC
		
		elif level == VERBOSE:
			output = bcolors.OKBLUE + output + bcolors.ENDC
		
		elif level == DEBUG:
			output = bcolors.HEADER + output + bcolors.ENDC
	
	print(output)

	if level == FATAL:
		exit(1)

	return None

def step(text = "", no = 0, max_no = 12, percentage = None):
	if percentage != None:
		log("[{:3d}%] {}".format(percentage, text), level=INFO)
	else:
		log("[{:3d}%] {}".format(int((no / max_no) * 100), text), level=INFO)

def substep(text = ""):
	log("       - {}".format(text), level=INFO)
 
def copy(src, dest):
	try:
		shutil.copytree(src, dest)
	except OSError as e:
		if e.errno == errno.ENOTDIR:
			shutil.copy(src, dest)
		else:
			print('Directory not copied. Error: %s' % e)