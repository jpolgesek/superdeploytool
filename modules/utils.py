#coding: utf-8
import shutil
import errno


def step(text = "", no = 0, max_no = 12):
	print("[{:3d}%] {}".format(int((no / max_no) * 100), text))

def substep(text = ""):
	print("       - {}".format(text))

 
def copy(src, dest):
	try:
		shutil.copytree(src, dest)
	except OSError as e:
		if e.errno == errno.ENOTDIR:
			shutil.copy(src, dest)
		else:
			print('Directory not copied. Error: %s' % e)