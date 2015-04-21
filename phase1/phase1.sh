#!/bin/bash
rm -r formslist
rm -r linkslist
python ./processpara.py $1
#cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
scrapy crawl example.com
python ./phase1.py
mv ./crawler/spiders/parameter.py /home/user/Assignment3/WebSecurity_Final/phase2_3/
mv phase1.json ../output/phase1_output.json
