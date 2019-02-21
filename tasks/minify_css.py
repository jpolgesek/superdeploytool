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

		utils.step("Minify CSS files", 3)
		css_input = ""
		css_count = 0

		with open(os.path.join(cfg.source_dir, cfg.source_css), "r", encoding="UTF-8") as f:
			for line in f.readlines():
				if len(line) < 5 or not line.startswith("@import"): continue
				
				line = line.strip()

				try:
					filename = re.search(r'''(@import url\(")(.*)("\);)''', line)[2]
					path = os.path.join(cfg.source_dir, "assets", "css", filename)

					with open(path, "r", encoding="UTF-8") as src:
						css_input += src.read() + "\n"
						css_count += 1
				except:
					pass

		css_compressed = csscompressor.compress(css_input)

		utils.substep("Before:\t {} kB in {} files ({} lines)".format(len(css_input)//1024, css_count, css_input.count("\n")))
		utils.substep("After: \t {} kB in 1 file ({} lines)".format(len(css_compressed)//1024, css_compressed.count("\n")+1))

		self.data["css_compressed"] = css_compressed
