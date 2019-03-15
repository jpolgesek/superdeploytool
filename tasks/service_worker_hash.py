#coding: utf-8
import os
import re
import hashlib

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

		utils.step("Generate unique build id for cache bust", percentage = self.data["current_step_percentage"])

		checksums = ""
		for path in cfg.hash_this:
			with open(os.path.join(cfg.output_dir, path), "r", encoding="UTF-8") as f:
				sha1 = hashlib.sha1()
				sha1.update(f.read().encode("utf-8"))
				checksums += sha1.hexdigest()
			utils.substep("Generated checksum for {}".format(path))
		try:
			with open(os.path.join(cfg.output_dir, "sw.js"), "r", encoding="UTF-8") as f:
				content = f.read()
				content = content.replace("var ENABLE_CACHE = false;", "var ENABLE_CACHE = true;")
				content = content.replace('%compiler_checksums%', checksums + cfg.version)
				content = content.replace('%build%', cfg.version)

				with open(os.path.join(cfg.output_dir, "sw.js"), "w", encoding="UTF-8") as f_new:
					f_new.write(content)
					utils.substep("Saved new service worker")
		except:
			return False