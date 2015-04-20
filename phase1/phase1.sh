#!/bin/bash
rm -r formslist
rm -r linkslist
python ./processpara.py ../config/$1
#cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
scrapy crawl example.com
python ./phase1.py
rm ./crawler/spiders/parameter.py
