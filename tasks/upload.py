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

		if self.cfg.upload_only or True:
			if target["uploader"] == "ftp":
				import modules.upload_ftp
				uploader = modules.upload_ftp.Uploader(target["hostname"])
				uploader.login(
					target["ftp"]["username"], 
					target["ftp"]["password"]
					)
			elif target["uploader"] == "scp":
				import modules.upload_scp
				uploader = modules.upload_scp.Uploader(target["hostname"])
				uploader.login(
					target["scp"]["username"], 
					target["scp"]["password"]
					)
			elif target["uploader"] == "local":
				import modules.upload_local
				uploader = modules.upload_local.Uploader(target["hostname"])
			else:
				print("No such uploader: {}".format(target["uploader"]))
				exit(1)

			#FIXME
			target["rootdir_app"] = target[target["uploader"]]["rootdir_app"]
			target["rootdir_manifest"] = target[target["uploader"]]["rootdir_manifest"]

			uploader.connect()

			utils.log("Show update screen on {}".format(target["hostname"]), level=utils.INFO)
			uploader.chdir(target["rootdir_app"])
			uploader.upload_file(os.path.join(cfg.output_dir, "update.html"), "index.html")

			try:
				utils.log("Upload manifest to {}".format(target["hostname"]), level=utils.INFO)
				uploader.connect()
				uploader.chdir(target["rootdir_manifest"])
				uploader.upload_file(os.path.join(cfg.output_dir, "manifest.json"), "manifest.json")
			except:
				utils.log("Manifest upload failed", level=utils.INFO)

			utils.log("Upload app build {} to {}".format(cfg.version, target["hostname"]), level=utils.INFO)
			uploader.chdir(target["rootdir_app"])
			uploader.upload_dir(cfg.output_dir, target["rootdir_app"])

			utils.log("Hide update screen on {}".format(target["hostname"]), level=utils.INFO)
			uploader.chdir(target["rootdir_app"])
			uploader.upload_file(os.path.join(cfg.output_dir, "index.html"), "index.html")

			utils.log("TODO: Notify clients about new version", level=utils.INFO)

		return True

	