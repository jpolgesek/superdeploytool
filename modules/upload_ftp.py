#coding: utf-8
import ftplib
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
		return None
	
	def login(self, username, password):
		self.username = username
		self.password = password
		return True
	
	def connect(self):
		self.ftp = ftplib.FTP(self.hostname)
		self.ftp.login(user = self.username, passwd = self.password)
		return True
	
	def chdir(self, directory):
		self.ftp.cwd(directory)
		return True
	
	def upload_file(self, source, target):
		return self.ftp.storbinary("STOR {}".format(target), open(source, 'rb'))
	
	def upload_dir(self, source, target):
		for root, dirs, files in os.walk(source, topdown=True):
			for name in files:
				self.ftp.cwd("/")
				self.ftp.cwd(target)

				path = os.path.join(root, name).split(source)[1]
				path = path.replace("\\", "/")

				subdirs = path.split("/")
				subdirs.pop(-1)

				for subdir in subdirs:
					try:
						self.ftp.mkd(subdir)
					except:
						pass
					self.ftp.cwd(subdir)
				
				if name in self.do_not_upload: continue
				
				try:
					self.ftp.storbinary("STOR {}".format(name), open(source + path, 'rb'))
					modules.utils.substep("File {} uploaded".format(path))
				except:
					modules.utils.substep("File {} was not uploaded".format(path))