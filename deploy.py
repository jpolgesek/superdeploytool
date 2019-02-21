#coding: utf-8
import re
import os
import json
import time
import shutil
import hashlib
import argparse
import subprocess
from pathlib import Path

import deployconfig
from modules import utils
from modules import versioning

user_data = None

try:
	with open(".user.json", "r", encoding = "UTF-8") as f:
		user_data = json.load(f)
	print("Loaded .user.json succesfully")
except:
	print("Failed to load .user.json")

parser = argparse.ArgumentParser()
parser.add_argument('--upload-static-assets', action='store_true')
parser.add_argument('--data-only', action='store_true')

parser.add_argument('--dev', action='store_true')
parser.add_argument('--http-rootdir-app')
parser.add_argument('--http-rootdir-manifest')
parser.add_argument('--hostname')
parser.add_argument('--uploader', help='One of: scp, ftp, local')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--uploader-rootdir-manifest')
parser.add_argument('--uploader-rootdir-app')
parser.add_argument('--path')
parser.add_argument('--upload-only', action='store_true')
parser.add_argument('--exec-before')
parser.add_argument('--exec-after')
parser.add_argument("app_name")
parser.add_argument("app_env")

args = parser.parse_args()

if args.path == None:
	args.app_env = args.app_name + "-" + args.app_env

	if user_data == None:
		print("No path and no .user.json, exiting")
		exit(1)

	elif args.app_name not in user_data["targets"]:
		print("No such profile {}".format(args.app_name))
		exit(1)

	elif args.app_name not in user_data["targets"]:
		print("No such profile {}".format(args.app_name))
		exit(1)

	elif args.app_env not in user_data["targets"][args.app_name]["envs"] or args.app_env not in user_data["envs"]:
		print("No such env {}".format(args.app_env))
		exit(1)

	print("[Using .user.json]")
	
	app = user_data["targets"][args.app_name]
	env = user_data["envs"][args.app_env]

	for possible_path in app["web-paths"]:
		path = Path(possible_path)
		if not path.is_dir():
			print("no such file or directory")
			exit(1)
		
		path = Path(possible_path + "/.deploytool.json")
		if not path.exists():
			print("No deploytool config. EXIT?")
			exit(1)
		
		args.path = possible_path

elif args.upload_only:
	print("[Upload only mode]")
	
	args.app_env = args.app_name + "-" + args.app_env
	env = user_data["envs"][args.app_env]
	app = {
			"web-paths": [args.path],
			"envs": [""]
	}

else:
	if None in (args.uploader, args.http_rootdir_app, args.hostname, args.uploader, args.uploader_rootdir_app):
		print("Not enough args :(")
		exit(1)
	
	print("[Using provided path]")

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
	print("Loaded .deploytool.json succesfully")
except:
	print("Failed to load .deploytool.json")


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
if args.upload_only:
	cfg.upload_only = True
cfg.target = target
cfg.exec_after = args.exec_after


tasks_list = [
	"exec_before",
	"prepare_build_directory",
	"copy_static",
	"minify_css",
	"minify_js",
	"write_minified_files",
	"prepare_manifest",
	"service_worker_hash",
	"upload",
	"cleanup",
	"exec_after"
]

for current_task in tasks_list:
	print("---Running task: {}---".format(current_task))
	task = getattr(tasks, current_task).Task(cfg, utils, data)
	task.run()