#coding: utf-8
import argparse

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
parser.add_argument('--use-colors', action='store_true')
parser.add_argument("app_name")
parser.add_argument("app_env")

args = parser.parse_args()