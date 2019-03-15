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

		if cfg.remove_output_after_build and os.path.exists(cfg.output_dir):
			shutil.rmtree(cfg.output_dir)
			utils.step("Removed build directory - {}".format(cfg.output_dir), percentage = self.data["current_step_percentage"])
		
		return True