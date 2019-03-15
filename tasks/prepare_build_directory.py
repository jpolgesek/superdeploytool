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
		self.utils.step("Cleanup build directory", percentage = self.data["current_step_percentage"])

		if os.path.exists(self.cfg.output_dir): 
			shutil.rmtree(self.cfg.output_dir)
			self.utils.substep("Removed build directory - {}".format(self.cfg.output_dir))
			
		os.makedirs(self.cfg.output_dir)
		self.utils.substep("Created build directory - {}".format(self.cfg.output_dir))
		return True