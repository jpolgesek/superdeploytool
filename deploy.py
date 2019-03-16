#coding: utf-8
import os
import re
import json
import hashlib
from pathlib import Path

import deployconfig
from modules import utils
from modules import argparser
from modules import versioning

args = argparser.args

if args.use_colors:
	utils.USE_COLORS = True


user_data = None

try:
	with open(".user.json", "r", encoding = "UTF-8") as f:
		user_data = json.load(f)
	utils.log("Loaded .user.json", level = utils.INFO)
except:
	utils.log("Failed to load .user.json", level = utils.INFO)


if args.path == None:
	args.app_env = args.app_name + "-" + args.app_env

	if user_data == None:
		utils.log("No path and no .user.json, exiting", level = utils.FATAL)

	elif args.app_name not in user_data["targets"]:
		utils.log("No such profile {}".format(args.app_name), level = utils.FATAL)
	
	elif args.app_env not in user_data["targets"][args.app_name]["envs"] or args.app_env not in user_data["envs"]:
		utils.log("No such env {}".format(args.app_env), level = utils.FATAL)

	utils.log("Using .user.json", level = utils.INFO)
	
	app = user_data["targets"][args.app_name]
	env = user_data["envs"][args.app_env]

	for possible_path in app["web-paths"]:
		path = Path(possible_path)
		if not path.is_dir():
			utils.log("No such file or directory: {}".format(str(path)), level = utils.INFO)
		
		path = Path(possible_path + "/.deploytool.json")
		if not path.exists():
			utils.log("No deploytool config at: {}".format(str(path)), level = utils.INFO)
		
		args.path = possible_path
	
	
elif args.upload_only:
	utils.log("Upload only mode", level = utils.WARNING)
	
	args.app_env = args.app_name + "-" + args.app_env
	env = user_data["envs"][args.app_env]
	app = {
			"web-paths": [args.path],
			"envs": [""]
	}

else:
	if None in (args.uploader, args.http_rootdir_app, args.hostname, args.uploader, args.uploader_rootdir_app):
		utils.log("Not enough arguments", level = utils.FATAL)
	
	utils.log("Using provided path", level = utils.INFO)

	if args.http_rootdir_manifest == None: 
		args.http_rootdir_manifest = args.http_rootdir_app
	
	if args.uploader_rootdir_manifest == None: 
		args.uploader_rootdir_manifest = args.uploader_rootdir_app
		
	env = {
		"dev": args.dev,
		"http_rootdir_app": args.http_rootdir_app,
		"http_rootdir_manifest": args.http_rootdir_manifest,
		"hostname": args.hostname,
		"uploader": args.uploader,
		args.uploader: {
			"rootdir_app": args.uploader_rootdir_app,
			"rootdir_manifest": args.uploader_rootdir_manifest,
			"username": args.username,
			"password": args.password,
		}
	}

	app = {
			"web-paths": [args.path],
			"envs": ["n/a"]
	}


#wczytaj config z .deploytool.json
try:
	with open(str(Path(args.path + "/.deploytool.json")), "r", encoding = "UTF-8") as f:
		app_config = json.load(f)
	cfg = deployconfig.DeployConfig(Path(args.path), app_config)
	target = env
	utils.log("Loaded .deploytool.json succesfully", level = utils.INFO)
except:
	utils.log("Failed to load .deploytool.json", level = utils.INFO)


import tasks

# And here we go

version = versioning.get_version_string(dev = target['dev'])
safe_version = version
cfg.version = version

if args.data_only:
	cfg.static_files = ["data.json", "index.html", "update.html"]
	cfg.static_dirs = []

# Translate params for new task builder
data = {}
cfg.exec_before = args.exec_before
cfg.source_dir = str(cfg.source_dir)
cfg.always_upload_static |= args.upload_static_assets
cfg.target = target
cfg.exec_after = args.exec_after

try :
	a = open(os.path.join(cfg.output_dir, str(cfg.source_html).replace("index", "ie_index")), "r")
	a.close()
	cfg.static_files.append("ie_index.html")
except:	
	pass

if args.upload_only or args.data_only:
	cfg.upload_only = True
	tasks_list = [
		"exec_before",
		"prepare_build_directory",
		"copy_static",
		"upload",
		"cleanup",
		"exec_after"
	]
else:
	tasks_list = [
		"exec_before",
		"prepare_build_directory",
		"copy_static",
		"minify_css",
		"minify_js",
		"write_minified_files",
		"check_for_ie",
		"$data['ie_build'] != None$minify_css",
		"$data['ie_build'] != None$minify_js",
		"$data['ie_build'] != None$write_minified_files",
		"prepare_manifest",
		"service_worker_hash",
		"upload",
		"cleanup",
		"exec_after"
	]

data["total_step_count"] = len(tasks_list)

for i, current_task in enumerate(tasks_list):
	run_task = True
	data["current_step_id"] = i
	data["current_step_percentage"] = int((data["current_step_id"] / data["total_step_count"]) * 100)
	utils.current_percentage = data["current_step_percentage"] 

	if current_task.find("$") != -1:
		condition = current_task.split("$")[1]
		current_task = current_task.split("$")[2]
		if eval(condition):
			utils.log("Condition '{}' met for task {}".format(condition, current_task), level = utils.INFO)
		else:
			utils.log("Condition '{}' not met for task {}".format(condition, current_task), level = utils.INFO)
			run_task = False
	
	if run_task:
		utils.log("Task: {}".format(current_task), level = utils.INFO)

		task = getattr(tasks, current_task).Task(cfg, utils, data)
		
		try:
			task.run()
		except Exception as e:
			utils.log("Task has failed: {}.".format(str(e)), level = utils.FATAL)
		