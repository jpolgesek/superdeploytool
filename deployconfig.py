#coding: utf-8
from pathlib import Path

class DeployConfig:
	def __init__(self, path, data):
		self.relative = False
		self.path = path
		self.source_dir = str(path)
		self.output_dir = "output"
		self.always_upload_static = True
		self.remove_output_after_build = True
		self.static_dirs = []
		self.static_files = []

		if "type" in data and data["type"] == "upload_only":
			self.upload_only = True
			self.static_files = data["files"]
			return
		else:
			self.upload_only = False
		
		self.source_basedir = data["source_basedir"]

		self.remove_output_after_build = data["remove_output_after_build"]
		self.source_update_html = data["source_update_html"]
		self.always_upload_static = data["always_upload_static"]

		self.output_dir = self._gen_path(data["output_dir"])
		self.source_css = self._gen_path(data["source_css"])
		self.source_html = self._gen_path(data["source_html"])
		self.raw_source_html = data["source_html"]
		self.static_dirs = data["static_dirs"]
		self.static_files = data["static_files"]
		self.hash_this = data["hash_this"]

		self.relative = True
		self.static_dirs[:] = map(self._gen_path, self.static_dirs)
		self.static_files[:] = map(self._gen_path, self.static_files)
		self.hash_this[:] = map(self._gen_path, self.hash_this)
			
		self.variables = data["variables"]

		return None
	
	def _gen_path(self, arr):
		if type(arr) == type([]):
			arr.insert(0, self.source_basedir)
			if not self.relative:
				arr.insert(0, str(self.path))
			arr = Path("/".join(arr))
			
		return arr