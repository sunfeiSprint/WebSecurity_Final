#!/bin/bash
cp './crawler/spiders'$1 ./crawler/spiders/parameter.py
scrapy crawl example.com
python ./phase1.py
