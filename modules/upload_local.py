#coding: utf-8
import shutil 
import modules.utils
import os
class Uploader:
	do_not_upload = [
		"manifest.json",
		"index.html",
		"update.html"
	]

	def __init__(self, hostname):
		self.hostname = hostname
		return
			
	def connect(self):
		return

	def chdir(self, directory):
		self.cd = directory
		return

	def copytree(self, src, dst, symlinks=False, ignore=None): 
		for item in os.listdir(src): 
			s = os.path.join(src, item) 
			d = os.path.join(dst, item) 
			if os.path.isdir(s): 
				if os.path.isdir(d): 
					self.copytree(s, d, symlinks, ignore) 
				else: 
					shutil.copytree(s, d, symlinks, ignore) 
			else: 
				shutil.copy2(s, d)

	def upload_file(self, source, target):
		target = os.path.join(self.cd, target)
		try:
			shutil.copyfile(source, target)
		except:
			pass
		return

	def upload_dir(self, source, target):
		target = os.path.join(self.cd, target)
		self.copytree(source, target)
		return