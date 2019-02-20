#coding: utf-8
import os
import time

def get_version_string(dev = False, safe = True):
	version = ["SDT-"]

	try:
		version.append(os.environ['GITLAB_TAG'].replace(".", ""))
	except:
		version.append("400")

	try:
		version.append(os.environ['CI_COMMIT_SHA'][:8])
	except:
		version.append("M")

	try:
		version.append(os.environ['CI_JOB_ID'][:8])
	except:
		version.append(str(int(time.time()))[-8:])

	if dev:
		version.append("DEV")

	if safe:
		return "-".join(version)
	else:
		return ".".join(version)