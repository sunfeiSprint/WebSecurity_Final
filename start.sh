#!/bin/bash

# Before you run this script
# You need to modify the config file to configure:
# - loginflag(whether login is needed )
# - login_url
# - start_url
# - username
# - password

config_file=$1

if [ -f $config_file ]
then
	# phase 1
	cd ./phase1
	sh phase1.sh "../$config_file"

	# phase 2 & 3
	cd ../phase2_3
	python phase2.py
	python phase3.py

	# phase 4
	cd ../phase4
	python generate_exploit.py -c "../$config_file" -i ../output/phase3_output.json -o ../exploit_scripts
else
	echo "Please provide a valid config file in JSON format"
fi
