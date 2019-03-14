#coding: utf-8
import os

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

		try :
			a = open(str(cfg.source_html).replace("index", "ie_index"), "r")
			a.close()
			self.data['ie_build'] = True
		except:		
			self.data['ie_build'] = None

		cfg.source_css = str(cfg.source_css).replace("css", "ie_css").replace(".ie_css", ".css")
		cfg.source_html = str(cfg.source_html).replace("index", "ie_index")

		return True