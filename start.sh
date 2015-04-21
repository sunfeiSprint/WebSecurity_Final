#!/bin/bash

##You need to modify the config.json to configure loginflag(whether login is needed ) login_url ,start_url ,username ,password
##Before you run this script

cd ./phase1
sh phase1.sh
cd ../phase2_3
python phase2.py
python phase3.py

#cd ../phase4
#python generate_exploit.py -c ../config/config.json -i ../output/phase3.json -o ../output/

