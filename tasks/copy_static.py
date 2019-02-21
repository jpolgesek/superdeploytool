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

		if cfg.always_upload_static:
			for path in cfg.static_dirs:
				path = str(path)
				utils.copy(os.path.join(cfg.source_dir, path), os.path.join(cfg.output_dir, path))
				utils.substep("Copied dir - {}".format(path))
		else:
				utils.substep("Not copying static assets, use --upload-static-assets to force")


		for path in cfg.static_files:
			path = str(path)
			shutil.copyfile(os.path.join(cfg.source_dir, path), os.path.join(cfg.output_dir, path))
			utils.substep("Copied file - {}".format(path))
