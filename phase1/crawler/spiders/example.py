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
import Cookie
from scrapy.contrib.linkextractors import LinkExtractor
#from scrapy.http.cookies import CookieJar
class ExampleSpider(CrawlSpider):
    name = 'example.com'
    start_urls = parameter.login_urls
    startCrawlingURL = parameter.start_urls
    allowed_dommains= parameter.domain
    login_user = parameter.username
    login_pass = parameter.password
    cookie= Cookie.SimpleCookie()
    #rules = (Rule(LinkExtractor(deny=('logout\.php', ))),)
    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def start_requests(self):
        if parameter.login==True:
            return [Request(url=self.start_urls[0],method='get', dont_filter=True,callback=self.login)]
    def login(self,response):  
            args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
            print args,url,method
            print args
            argsdict={}
            for i in args:
                argsdict[i[0]]=i[1]
            print argsdict
            #args={'username':'scanner1', 'password':'scanner1'}
            return FormRequest(url,formdata=args, dont_filter=True,callback=self.after_login)
            #print args
            #print response.request
            #print response.request
            #return FormRequest.from_response(
            #    response,
            #    formdata=argsdict,
            #    dont_filter=True,
            #    callback=self.after_login
            #)
        #else:
        #    return Request(
        #        response.url,
        #        callback=self.parse_page
        #    )

    def after_login(self, response):
        # check login succeed before going on
        #print response.body
        if "No match"  in response.body:
            self.log("Login fail", level=log.ERROR)
            return


        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            #print response.body
            return Request(url=response.url,dont_filter=True)
            
            #return Request(url="https://app1.com/cart/review.php",
            #               callback=self.parse)

    # example of crawling all other urls in the site with the same
    # authenticated session.
    '''def parse(self,response):
        print "aaaaa"
        print response.url'''

  
    def parse(self, response):
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

            if link.find("logout") >-1 :
                continue
            if link.find("http") > -1:
                if link.find(parameter.domain[0])>-1:
                    print link
                    yield Request(url=link ,dont_filter=True,callback=self.parse)
                else:
                    continue
            elif len(link)>0 and link[0]=='#':
                if  (len(link)>1 and link[1]=='/') or len(link)==1:
                    print response.url+link[1:]
                    yield Request(url=response.url+link[1:],dont_filter=True, callback=self.parse)
                else:
                    print response.url+'/'+link[1:]
                    yield Request(url=response.url+'/'+link[1:],dont_filter=True, callback=self.parse)
            else:
                if (len(link)>0 and link[0]!='/') or len(link)==0:
                    print parameter.domain[0]+'/'+link
                    yield Request(url=parameter.domain[0]+'/'+link,dont_filter=True,callback=self.parse)
                else:
                    print parameter.domain[0]+link 
                    yield Request(url=parameter.domain[0]+link,dont_filter=True,callback=self.parse)
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