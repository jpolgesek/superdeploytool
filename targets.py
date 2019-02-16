#coding: utf-8
try:
	import raw_secrets as sec
except:
	import env_secrets as sec

targets = {}

targets["zastepstwa.zseil.pl"] = {
	"dev": True,
	"http_rootdir_app": "/",
	"http_rootdir_manifest": "/",
	"hostname": "zastepstwa.zseil.pl",
	"upload": True,
	"uploader": "scp",
	"scp": {
		"rootdir_manifest": "/var/www/zseil/zastepstwa/",
		"rootdir_app": "/var/www/zseil/zastepstwa/"
	}
}

targets["testpc"] = {
	"dev": True,
	"http_rootdir_app": "/",
	"http_rootdir_manifest": "/",
	"hostname": "localhost",
	"upload": True,
	"uploader": "local",
	"local": {
		"rootdir_manifest": "C:\\xampp\\htdocs\\lap-htdocs\\zseilplan_localtest\\",
		"rootdir_app": "C:\\xampp\\htdocs\\lap-htdocs\\zseilplan_localtest\\"
	},
}

targets["testlap"] = {
	"dev": True,
	"http_rootdir_app": "/",
	"http_rootdir_manifest": "/",
	"hostname": "localhost",
	"upload": True,
	"uploader": "local",
	"local": {
		"rootdir_manifest": "C:\\xampp\\htdocs\\lap-htdocs\\zseilplan_localprod\\",
		"rootdir_app": "C:\\xampp\\htdocs\\lap-htdocs\\zseilplan_localprod\\"
	},
}

sec.add_passwords_targets(targets)