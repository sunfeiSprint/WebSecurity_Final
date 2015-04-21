#!/bin/bash

# Before you run this script
# You need to modify the config.json to configure:
# - loginflag(whether login is needed )
# - login_url
# - start_url
# - username
# - password

# phase 1
cd ./phase1
sh phase1.sh

# phase 2 & 3
cd ../phase2_3
python phase2.py
python phase3.py

# phase 4
cd ../phase4
python generate_exploit.py -c ../config/config.json -i ../output/phase3_output.json -o ../exploit_scripts
