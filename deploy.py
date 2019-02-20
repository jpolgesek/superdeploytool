#coding: utf-8
import re
import os
import json
import time
import shutil
import hashlib
import htmlmin
import argparse
import subprocess
import csscompressor
from pathlib import Path
from jsmin import jsmin
from html.parser import HTMLParser

import deployconfig
from modules import utils

user_data = None

try:
	with open(".user.json", "r", encoding = "UTF-8") as f:
		user_data = json.load(f)
	print("loading .user.json ok")
except:
	print("failed .user.json")

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
	print("TODO2")
	args.app_env = args.app_name + "-" + args.app_env
	env = user_data["envs"][args.app_env]
	app = {
			"web-paths": [args.path],
			"envs": [""]
	}

else:
	print("TODO")
	if None in (args.uploader, args.http_rootdir_app, args.hostname, args.uploader, args.uploader_rootdir_app):
		print("Not enough args :(")
		exit(1)
	
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
			"web-paths": ["D:\\SHARED_TODO\\autosync\\lap-htdocs\\supercleverzastepstwa"],
			"envs": ["zastepstwa-dev"]
	}






#wczytaj config z .deploytool.json
with open(str(Path(args.path + "/.deploytool.json")), "r", encoding = "UTF-8") as f:
	app_config = json.load(f)

cfg = deployconfig.DeployConfig(Path(args.path), app_config)
target = env




# And here we go

version = "SDT-"

try:
	version += os.environ['GITLAB_TAG'].replace(".", "")
except:
	version += "400"

try:
	version += "."
	version += os.environ['CI_COMMIT_SHA'][:8]
except:
	version += "M"

try:
	version += "."
	version += os.environ['CI_JOB_ID'][:8]
except:
	version += str(int(time.time()))[-8:]


if target['dev']:
	version += ".DEV"

safe_version = version.replace(".", "-")
		
print(version)



if args.data_only:
	cfg.static_files = ["data.json", "index.html", "update.html"]
	cfg.static_dirs = []


if args.exec_before != None:
	utils.step("Exec before", 0.5)
	process = subprocess.Popen(args.exec_before, shell=True, stdout=subprocess.PIPE)
	process.wait()


# --- STEP 1
# --- Prepare clean build directory
utils.step("Cleanup build directory", 1)

if os.path.exists(cfg.output_dir): 
	shutil.rmtree(cfg.output_dir)
	utils.substep("Removed build directory - {}".format(cfg.output_dir))
	
os.makedirs(cfg.output_dir)
utils.substep("Created build directory - {}".format(cfg.output_dir))

'''
os.makedirs(os.path.join(cfg.output_dir, "assets", "css"))
os.makedirs(os.path.join(cfg.output_dir, "assets", "js"))
utils.substep("Created build assets subdirectory ")
'''


cfg.source_dir = str(cfg.source_dir)

# --- STEP 2
# --- Copy static files to build directory
utils.step("Copy static files to build directory", 2)

if args.upload_static_assets or cfg.always_upload_static:
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




if cfg.upload_only or args.upload_only:
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

	uploader.connect()

	utils.step("Upload Super Clever Zastepstwa build {} to {}".format(version, target["hostname"]), 9)
	uploader.chdir(target["rootdir_app"])
	uploader.upload_dir(cfg.output_dir, target["rootdir_app"])

	utils.step("TODO: Notify clients about new version", 11)

	if cfg.remove_output_after_build and os.path.exists(cfg.output_dir):
		shutil.rmtree(cfg.output_dir)
		utils.step("Removed build directory - {}".format(cfg.output_dir), 12)
	
	if args.exec_after != None:
		utils.step("Exec after", 12)
		process = subprocess.Popen(args.exec_after, shell=True, stdout=subprocess.PIPE)
		process.wait()

	
	exit(0)



# --- STEP 3
# --- Minify CSS files
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



# --- STEP 4
# --- Minify JavaScript files
utils.step("Minify JavaScript files", 4)
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
js_compressed = "var ZSEILPLAN_BUILD = '{0}'; //Build {0} by superdeploytool.py (NEW) \n".format(version)
#js_compressed += jsmin(parser.output)
js_compressed += parser.output

utils.substep("Before:\t {} kB in {} files ({} lines)".format(len(parser.output)//1024, parser.count, parser.output.count("\n")))
utils.substep("After: \t {} kB in 1 file ({} lines)".format(len(js_compressed)//1024, js_compressed.count("\n")+1))





# --- STEP 5
# --- Write minified files to build directory
utils.step("Write minified files to build directory", 5)

js_path = Path("/".join([cfg.output_dir, "assets", "js", "c_app.js"]))
css_path = Path("/".join([cfg.output_dir, "assets", "css", "c_style.css"]))
js_path.parent.mkdir(parents=True, exist_ok=True)
css_path.parent.mkdir(parents=True, exist_ok=True)


with open(js_path, "w", encoding="UTF-8") as f:
	f.write(js_compressed)
	utils.substep("Saved compiled JavaScript to {}".format(js_path))

with open(css_path, "w", encoding="UTF-8") as f:
	f.write(css_compressed)
	utils.substep("Saved compiled CSS to {}".format(css_path))

with open(os.path.join(cfg.output_dir, cfg.source_html), "r+", encoding="UTF-8") as f:
	replaced = re.sub(r"(<!-- %compile_css_start%-->)([\s\S]*)(<!-- %compile_css_end%-->)", "<link rel='stylesheet' href='assets/css/c_style.css?ver={}'>".format(safe_version), f.read())
	replaced = re.sub(r"(<!-- %compile_js_start%-->)([\s\S]*)(<!-- %compile_js_end%-->)", "<script src='assets/js/c_app.js?ver={}'></script>".format(safe_version), replaced)
	if not target["dev"]: 
		replaced = replaced.replace("<!--%DEV_ONLY_START%-->", "<!--%DEV_ONLY_START% ")
		replaced = replaced.replace("<!--%DEV_ONLY_STOP%-->", " %DEV_ONLY_START% ")
	replaced = htmlmin.minify(replaced, remove_empty_space=True, remove_comments=True)
	f.seek(0)
	f.write(replaced)
	f.truncate()
	utils.substep("Updated index.html")


# Prepare manifest
with open(os.path.join(cfg.output_dir, "manifest.json"), 'r') as f:
	manifest = f.read()

if target["http_rootdir_app"] != "/": 
	manifest = manifest.replace(': "/', ': "{}/'.format(target["http_rootdir_app"]))
		
if target["dev"]: 
	manifest = manifest.replace('launcher-icon-4x.png', 'launcher-icon-test.png')
	manifest = manifest.replace('launcher-icon-512.png', 'launcher-icon-test.png')
	manifest = manifest.replace('Plan Lekcji', '[TEST] Plan Lekcji')
	manifest = manifest.replace('Super Clever Plan', '[TEST] Super Clever Plan')

with open(os.path.join(cfg.output_dir, "manifest.json"), 'w') as f:			
	f.write(manifest)
	
# --- STEP 5
# --- Write minified files to build directory
utils.step("Generate unique build id for cache bust", 6)
'''
checksums = ""
for path in cfg.hash_this:
	with open(os.path.join(cfg.output_dir, path), "r", encoding="UTF-8") as f:
		sha1 = hashlib.sha1()
		sha1.update(f.read().encode("utf-8"))
		checksums += sha1.hexdigest()
	utils.substep("Generated checksum for {}".format(path))

with open(os.path.join(cfg.output_dir, "sw.js"), "r", encoding="UTF-8") as f:
	content = f.read()
	content = content.replace("var ENABLE_CACHE = false;", "var ENABLE_CACHE = true;")
	content = content.replace('%compiler_checksums%', checksums + version)
	content = content.replace('%build%', version)

	with open(os.path.join(cfg.output_dir, "sw.js"), "w", encoding="UTF-8") as f_new:
		f_new.write(content)
		utils.substep("Saved new service worker")
'''


with open(os.path.join(cfg.output_dir, cfg.source_html), "r+", encoding="UTF-8") as f:
	replaced = f.read().replace("%ver%", safe_version)
	replaced = htmlmin.minify(replaced, remove_empty_space=True, remove_comments=True)
	f.seek(0)
	f.write(replaced)
	f.truncate()
	utils.substep("Updated index.html")


if True:
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

	utils.step("Show update screen on {}".format(target["hostname"]), 7)
	uploader.chdir(target["rootdir_app"])
	uploader.upload_file(os.path.join(cfg.output_dir, "update.html"), "index.html")

	
	utils.step("Upload manifest to {}".format(target["hostname"]), 8)
	uploader.connect()
	uploader.chdir(target["rootdir_manifest"])
	uploader.upload_file(os.path.join(cfg.output_dir, "manifest.json"), "manifest.json")
	

	utils.step("Upload Super Clever Zastepstwa build {} to {}".format(version, target["hostname"]), 9)
	uploader.chdir(target["rootdir_app"])
	uploader.upload_dir(cfg.output_dir, target["rootdir_app"])

	utils.step("Hide update screen on {}".format(target["hostname"]), 10)
	uploader.chdir(target["rootdir_app"])
	uploader.upload_file(os.path.join(cfg.output_dir, "index.html"), "index.html")

	utils.step("TODO: Notify clients about new version", 11)

if cfg.remove_output_after_build and os.path.exists(cfg.output_dir):
	shutil.rmtree(cfg.output_dir)
	utils.step("Removed build directory - {}".format(cfg.output_dir), 12)



if args.exec_after != None:
	utils.step("Exec after", 12)
	process = subprocess.Popen(args.exec_after, shell=True, stdout=subprocess.PIPE)
	process.wait()