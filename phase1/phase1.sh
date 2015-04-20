#!/bin/bash
rm -r formslist
rm -r linkslist
cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
scrapy crawl example.com
python ./phase1.py
rm ./crawler/spiders/parameter.py
