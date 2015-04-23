#!/bin/bash
rm -r formslist
rm -r linkslist
rm -r ../crawlernologin/formslist
rm -r ../crawlernologin/linkslist
python ./processpara.py $1
timeout 120 scrapy crawl example.com
cp ./crawler/spiders/parameter.py ../crawlernologin/crawlernologin/spiders/parameter.py
cd ../crawlernologin
timeout 120 scrapy crawl example.com1
cd ../phase1
python ./phase1.py
mv ./crawler/spiders/parameter.py ../phase2_3/parameter.py
