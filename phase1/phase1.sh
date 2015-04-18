#!/bin/bash
cp './crawler/spiders/'$1 ./crawler/spiders/parameter.py
echo './crawler/spiders/'$1
scrapy crawl example.com
python ./phase1.py
rm ./crawler/spiders/parameter.py
