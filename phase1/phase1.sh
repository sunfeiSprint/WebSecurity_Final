#!/bin/bash
rm -r formslist
rm -r linkslist
echo $1
python ./processpara.py $1
#cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
timeout 45 scrapy crawl example.com
python ./phase1.py
rm ./crawler/spiders/parameter.py
