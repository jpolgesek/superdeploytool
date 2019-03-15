#coding: utf-8
try:
	import raw_secrets as sec
except:
	import env_secrets as sec

targets = {}

targets["example.com"] = {
	"dev": True,
	"http_rootdir_app": "/",
	"http_rootdir_manifest": "/",
	"hostname": "example.com",
	"upload": True,
	"uploader": "scp",
	"scp": {
		"rootdir_manifest": "/var/www/example/",
		"rootdir_app": "/var/www/example/"
	}
}

sec.add_passwords_targets(targets)