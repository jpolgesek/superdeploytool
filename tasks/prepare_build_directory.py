#coding: utf-8
import os
import shutil

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

		utils.log("Cleanup build directory", level=utils.INFO)

		if os.path.exists(cfg.output_dir): 
			shutil.rmtree(cfg.output_dir)
			utils.substep("Removed build directory - {}".format(cfg.output_dir))
			
		os.makedirs(self.cfg.output_dir)
		utils.substep("Created build directory - {}".format(cfg.output_dir))
		return True