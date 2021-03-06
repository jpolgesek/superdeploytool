#coding: utf-8
import os
import re
import shutil
import htmlmin
from pathlib import Path

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

		utils.log("Write minified files to build directory", level=utils.INFO)

		if 'ie_build' in self.data and self.data['ie_build'] != None:
			js_path = Path("/".join([cfg.output_dir, "assets", "ie_js", "c_app.js"]))
			css_path = Path("/".join([cfg.output_dir, "assets", "ie_css", "c_style.css"]))
		else:
			js_path = Path("/".join([cfg.output_dir, "assets", "js", "c_app.js"]))
			css_path = Path("/".join([cfg.output_dir, "assets", "css", "c_style.css"]))
		
		js_path.parent.mkdir(parents=True, exist_ok=True)
		css_path.parent.mkdir(parents=True, exist_ok=True)


		with open(str(js_path), "w", encoding="UTF-8") as f:
			f.write(self.data["js_compressed"])
			utils.substep("Saved compiled JavaScript to {}".format(js_path))

		with open(str(css_path), "w", encoding="UTF-8") as f:
			f.write(self.data["css_compressed"])
			utils.substep("Saved compiled CSS to {}".format(css_path))

		with open(os.path.join(str(cfg.output_dir), str(cfg.source_html)), "r+", encoding="UTF-8") as f:
				
			if 'ie_build' in self.data and self.data['ie_build'] != None:
				replaced = re.sub(r"(<!-- %compile_css_start%-->)([\s\S]*)(<!-- %compile_css_end%-->)", "<link rel='stylesheet' href='assets/ie_css/c_style.css?ver={}'>".format(cfg.version), f.read())
				replaced = re.sub(r"(<!-- %compile_js_start%-->)([\s\S]*)(<!-- %compile_js_end%-->)", "<script src='assets/ie_js/c_app.js?ver={}'></script>".format(cfg.version), replaced)
			else:
				replaced = re.sub(r"(<!-- %compile_css_start%-->)([\s\S]*)(<!-- %compile_css_end%-->)", "<link rel='stylesheet' href='assets/css/c_style.css?ver={}'>".format(cfg.version), f.read())
				replaced = re.sub(r"(<!-- %compile_js_start%-->)([\s\S]*)(<!-- %compile_js_end%-->)", "<script src='assets/js/c_app.js?ver={}'></script>".format(cfg.version), replaced)
			
			if not target["dev"]: 
				replaced = replaced.replace("<!--%DEV_ONLY_START%-->", "<!--%DEV_ONLY_START% ")
				replaced = replaced.replace("<!--%DEV_ONLY_STOP%-->", " %DEV_ONLY_START% ")
			
			replaced = replaced.replace("<!--%DEPLOYTOOL_ENABLE_START%", "")
			replaced = replaced.replace("%DEPLOYTOOL_ENABLE_END%-->", "")
			
			replaced = replaced.replace("%build%", cfg.version)
			replaced = replaced.replace("%ver%", cfg.version)

			replaced = htmlmin.minify(replaced, remove_empty_space=True, remove_comments=True)
			f.seek(0)
			f.write(replaced)
			f.truncate()
			utils.substep("Updated index.html")
