# Super Deploy Tool
Unified tool to deploy apps from "Super Clever" family

## Project preparation
(how to write .deploytool.json)
(how to write js)
(how to write html)
(how to write css)

## Deployment
**Profiles defined in .user.json in SDT directory**  
`python3 deploy.py zseilplan prod`  

**Profile defined in .deploytool.json**  
`python3 deploy.py --path [PATH TO APP] prod`  

**Profile defined in external file**  
`python3 deploy.py --path [PATH TO APP] --profile-file profile-zastepstwa.json --profile prod`  

**Profile defined with parameters**  
`python3 deploy.py --path [PATH TO APP] --dev --http-rootdir-app=/ --http-rootdir-manifest=/ --hostname=zastepstwa.zseil.pl --uploader=scp --uploader-rootdir-manifest=/var/www/zseil/zastepstwa/ --uploader-rootdir-app=/var/www/zseil/zastepstwa/ --exec-before ./test --exec-after calc`  
