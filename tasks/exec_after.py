#coding: utf-8
import os
import subprocess

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

		if cfg.exec_after != None:
			utils.step("Exec after", 12)
			process = subprocess.Popen(cfg.exec_after, shell=True, stdout=subprocess.PIPE)
			process.wait()

		return True