#coding: utf-8
import os
import re
import shutil
import csscompressor
from html.parser import HTMLParser
from jsmin import jsmin

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

		utils.log("Minify JavaScript files", level=utils.INFO)
		# TODO: separate build for IE

		class JSFinder(HTMLParser):
			output = ""
			count = 0
			def handle_starttag(self, tag, attrs):
				if tag != "script": return
				
				path = False
				
				for attr in attrs:
					if attr[0] == "src":
						path = attr[1].split("#")[0].split("?")[0]
						path = os.path.join(cfg.source_dir, path)
				
				if not path: return
				if "//" in path: return

				with open(path, "r", encoding="UTF-8") as f:
					self.output += f.read() + "\n"
					self.count += 1

		parser = JSFinder()

		with open(os.path.join(cfg.output_dir, cfg.source_html), "r", encoding="UTF-8") as f:
			parser.feed(f.read())

		#TODO: date
		js_compressed = "var ZSEILPLAN_BUILD = '{0}'; //Build {0} by superdeploytool.py (NEW) \n".format(cfg.version)
		js_compressed += jsmin(parser.output, quote_chars="'\"`")
		#js_compressed += parser.output

		utils.substep("Before:\t {} kB in {} files ({} lines)".format(len(parser.output)//1024, parser.count, parser.output.count("\n")))
		utils.substep("After: \t {} kB in 1 file ({} lines)".format(len(js_compressed)//1024, js_compressed.count("\n")+1))

		self.data["js_compressed"] = js_compressed

