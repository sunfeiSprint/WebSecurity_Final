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
    #handle_httpstatus_list = [404]
    name = 'example.com'
    start_urls = parameter.login_urls
    startCrawlingURL = parameter.start_urls
    allowed_dommains= parameter.domain
    login_user = parameter.username
    login_pass = parameter.password
    #cookie= Cookie.SimpleCookie()
    #rules = (Rule(LinkExtractor(deny=('logout\.php', ))),)
    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def start_requests(self):
        if parameter.login==True:
            return [Request(url=self.start_urls[0],method='get', dont_filter=True,callback=self.login)]
        else:
            return [Request(url=self.startCrawlingURL[0],method='get', dont_filter=True,callback=self.parse)]
    def login(self,response):
            
            args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
            print args,url,method
            #print args
            argsdict={}
            for i in args:
                argsdict[i[0]]=i[1]
            #print argsdict
            return FormRequest(url,formdata=args, dont_filter=True,callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        #print response.body
        if "No match"  in response.body:
            self.log("Login fail", level=log.ERROR)
            return []


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
        print response.body'''

  
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
            #print "THIS IS A LINK" + link
            #only process external/full link
#            cookie.load(response.headers['Set-Cookie'])
            if link.find("logout") >-1 :
                continue
            if link.find("http") > -1:
                if link.find(parameter.domain[0])>-1:
                    #print link
                    yield Request(url=link)
                else:
                    continue


            elif len(link)>0 and link[0]=='#':
                direct=response.url.split('/')
                if  (len(link)>1 and link[1]=='/') or len(link)==1:
                    #print response.url+link[1:]
                    yield Request(url=response.url+link[1:])
                else:
                    if response.url[-1:]!='/':
                        #print response.url+'/'+link[1:]
                        yield Request(url=response.url+'/'+link[1:])
                    else:
                        #print response.url+link[1:]
                        yield Request(url=response.url+link[1:])

            else:
                if (len(link)>0 and link[0]!='/') or len(link)==0:
                    direct=response.url.split('/')
                    path=''
                    for i in range(len(direct)-1):
                        path=path+direct[i]+'/'
                    #print path+link
                    yield Request(url=path+link)
                else:
                    #print parameter.domain[0]+link 
                    yield Request(url=parameter.domain[0]+link)
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
        #formsaction = hxs.select('//form/@action').extract()
        #print formsaction
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