#!/bin/bash
rm -r formslist
rm -r linkslist
echo $1
python ./processpara.py $1
#cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
timeout 45 scrapy crawl example.com
python ./phase1.py
mv ./crawler/spiders/parameter.py ../phase2_3/parameter.py
