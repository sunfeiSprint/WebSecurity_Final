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
from scrapy.http.cookies import CookieJar
class ExampleSpider(CrawlSpider):
    name = 'example.com'
    start_urls = parameter.login_urls
    startCrawlingURL = parameter.start_urls
    allowed_dommains= parameter.domain
    login_user = parameter.username
    login_pass = parameter.password
    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def parse(self, response):
        if parameter.login==True:
            args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
            #return FormRequest(url, method=method, formdata=args, callback=self.after_login)
            #args={'username':'admin', 'password':'admin'}
            #print args
            argsdict={}
            print response.headers
            for i in args:
                argsdict[i[0]]=i[1]
            print argsdict
            #print response.request
            return FormRequest.from_response(
                response,
                formdata=argsdict,
                dont_filter=True,
                meta = {'dont_merge_cookies': True},
                callback=self.after_login
            )
        else:
            #args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
            return Request(
                response.url,
                meta = {'dont_merge_cookies': True},
                callback=self.parse_page
            )

    def after_login(self, response):
        # check login succeed before going on
        if "ERROR: Invalid username" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)

            
            print cookieJar
            return Request(url=self.startCrawlingURL[0],
                           callback=self.parse_page)

    # example of crawling all other urls in the site with the same
    # authenticated session.
    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        hxs = HtmlXPathSelector(response)
        # i = CrawlerItem()
        # find all the link in the <a href> tag

        links = hxs.xpath('//a/@href').extract()
        #forms = hxs.select('//form').extract()
        self.extract_forms(hxs,response)
        
        # Yield a new request for each link we found
        # #this may lead to infinite crawling...
        #print response.headers['Location']
        for link in links:
            print "THIS IS A LINK" + link
            #only process external/full link
            if link.find("http") > -1:
                if link.find(parameter.domain[0])>-1:
                    yield Request(url=link, callback=self.parse_page)
                else:
                    continue
            elif len(link)>0 and link[0]=='#':
                if  (len(link)>1 and link[1]=='/') or len(link)==1:
                    yield Request(url=response.url+link[1:], callback=self.parse_page)
                else:
                    yield Request(url=response.url+'/'+link[1:], callback=self.parse_page)
            else:
                if (len(link)>0 and link[0]!='/') or len(link)==0:
                    yield Request(url=parameter.domain[0]+'/'+link,callback=self.parse_page)
                else: 
                    yield Request(url=parameter.domain[0]+link,callback=self.parse_page)
        item = LinkItem()
        #if len(hxs.xpath('//title/text()').extract())>0:
        item["title"] = hxs.xpath('//title/text()').extract()[0]
        item["url"] = response.url
        yield self.collect_item(item)

    def collect_item(self, item):
        return item

    def extract_forms(self,hxs,response):
        #print response
        forms = hxs.xpath('//form').extract()
#        formsaction = hxs.select('//form/@action').extract()
#        formsname = hxs.select('//form/@name').extract()
#        formmethod = hxs.select('//form/@method').extract()
        formsfile=open('formslist','a')
        linksfile=open('linkslist','a')
        for form in forms:
            form = form.encode('utf-8').strip()
            linksfile.write(str(response)[5:-1])
            linksfile.write('\n')
            formsfile.write(form)
            formsfile.write('\n')
        formsfile.close()
        linksfile.close()