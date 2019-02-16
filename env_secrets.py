#coding: utf-8
import os

def add_passwords_targets(t):
	t["zastepstwa.zseil.pl"]["scp"]["user"] = os.environ["zastepstwa_zseil_pl_scp_user"]
	t["zastepstwa.zseil.pl"]["scp"]["pass"] = os.environ["zastepstwa_zseil_pl_scp_pass"]
	
	return t