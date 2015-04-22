# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawler'
COOKIES_ENABLED = True
IGORING_ENDEBUG= False 
BOT_VERSION = '1.0'
HTTPCACHE_ENABLED = False
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DEPTH_LIMIT= 5