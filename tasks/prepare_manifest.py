#coding: utf-8
import os
import re
import shutil
import csscompressor

class Task:
	def __init__(self, cfg, utils, data):
		self.cfg = cfg
		self.utils = utils
		self.data = data
		return None
	
	def run(self):
		target = self.cfg.target
		utils = self.utils
		cfg = self.cfg

		with open(os.path.join(cfg.output_dir, "manifest.json"), 'r') as f:
			manifest = f.read()

		if target["http_rootdir_app"] != "/": 
			manifest = manifest.replace(': "/', ': "{}/'.format(target["http_rootdir_app"]))
				
		if target["dev"]: 
			manifest = manifest.replace('launcher-icon-', 'launcher-icon-test-')
			manifest = manifest.replace('Plan Lekcji', 'Test Plan')
			manifest = manifest.replace('Super Clever Plan', 'Super Clever Test Plan')

		with open(os.path.join(cfg.output_dir, "manifest.json"), 'w') as f:			
			f.write(manifest)
		