from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import LinkItem
from scrapy.http import Request
import scrapy
from scrapy.http import FormRequest
from scrapy import log
import parameter
from loginform import fill_login_form
from bs4 import  BeautifulSoup
import os

class ExampleSpider(CrawlSpider):
    name = 'example.com'
    start_urls = parameter.login_urls
    login_user = parameter.username
    login_pass = parameter.password
    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def parse(self, response):
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
#        return FormRequest.from_response(
#            response,
#            formdata={'log': 'pw@example', 'pwd': 'password'},
#            callback=self.after_login
#        )

    def after_login(self, response):
        # check login succeed before going on
        if "ERROR: Invalid username" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            return Request(url=self.start_urls[0],
                           callback=self.parse_page)


    # example of crawling all other urls in the site with the same
    # authenticated session.
    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        hxs = HtmlXPathSelector(response)
        # i = CrawlerItem()
        # find all the link in the <a href> tag
        links = hxs.select('//a/@href').extract()

        self.extract_forms(hxs,response)
        
        # Yield a new request for each link we found
        # #this may lead to infinite crawling...
        for link in links:
            print "THIS IS A LINK" + link
            #only process external/full link
            if link.find("http") > -1:
                yield Request(url=link, callback=self.parse_page)
            else:
                yield Request(url=parameter.domain[0]+link,callback=self.parse_page)
        item = LinkItem()
        item["title"] = hxs.select('//title/text()').extract()[0]
        item["url"] = response.url
        yield self.collect_item(item)

    def collect_item(self, item):
        return item

    def extract_forms(self,hxs,response):
        forms = hxs.select('//form').extract()
        #formsaction = hxs.select('//form/@action').extract()
        #formsname = hxs.select('//form/@name').extract()
        #formmethod = hxs.select('//form/@method').extract()
        formsfile=open('formslist','a')
        linksfile=open('linkslist','a')
        for form in forms:
            linksfile.write(str(response)[5:-1])
            linksfile.write('\n')
            formsfile.write(form)
            formsfile.write('\n')
        formsfile.close()
        linksfile.close()