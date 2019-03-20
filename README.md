# Super Deploy Tool
Unified tool to deploy apps from "Super Clever" family

## Project preparation

### How to write JS
- Put all files in `./assets/js/` (starting with `app.js` with app object)
- Name them by their function or object name (eg. `datetime.js` or `app.datetime.js`)
- Include them in html using `<script src="./assets/js/app.datetime.js">`  
   **Remember that order of imports is important**
- Wrap JS imports between `<!-- %compile_js_start%-->` and `<!-- %compile_js_end%-->` html tags

### How to write CSS
- Put all files in `./assets/css/` (starting with empty `style.css`)
- Name them by their function or object name (eg. `menu.css`)
- Include them in style.css using `@import menu.css`  
   **Remember that order of imports is important**
- Include style file in html using `<link rel="stylesheet" href="./assets/css/style.css>` 
- Wrap this import between `<!-- %compile_css_start%-->` and `<!-- %compile_css_end%-->` html tags

### Example .deploytool.json
```json
{
	"remove_output_after_build": true,
	"output_dir": "output",

	"source_basedir": ".",
	"source_css": ["assets","css","style.css"],
	"source_html": "index.html",
	"source_update_html": "update.html",

	"always_upload_static": true,
	"static_dirs": [
		["assets","img"]
	],
	"static_files": [
		"index.html",
		"update.html"
	],

	"hash_this": [ 
		"index.html"
	],

	"variables": {
		"%dev%": true
	}
}

```

## Deployment
**Profiles defined in .user.json in SDT directory**  
`python3 deploy.py zseilplan prod`  

**Profile defined in .deploytool.json**  
`python3 deploy.py --path [PATH TO APP] prod`  

**Profile defined in external file**  
`python3 deploy.py --path [PATH TO APP] --profile-file profile-zastepstwa.json --profile prod`  

**Profile defined with parameters**  
`python3 deploy.py --path [PATH TO APP] --dev --http-rootdir-app=/ --http-rootdir-manifest=/ --hostname=zastepstwa.zseil.pl --uploader=scp --uploader-rootdir-manifest=/var/www/zseil/zastepstwa/ --uploader-rootdir-app=/var/www/zseil/zastepstwa/ --exec-before ./test --exec-after calc`  
