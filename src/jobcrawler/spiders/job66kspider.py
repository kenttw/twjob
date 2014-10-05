# -*- coding: utf-8 -*-
'''
Created on 2014年8月18日

@author: kent
'''

import urlparse
import re
import xml.etree.ElementTree
import lxml.html
import os
import time

import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy

from jobcrawler import utility
from jobcrawler.items import RawItem 


class Job66kSpider(scrapy.Spider):
    name = "66KJobSpider"
#     allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://66kjobs.tw/",
    ]

    def parse(self, response):
#         filename = response.url.split("/")[-2]
#         with open(filename, 'wb') as f:
#             f.write(response.body)
            
        hxs = HtmlXPathSelector(response)
        anchors = hxs.select('//a/@href').extract()
        for rel_url in anchors:
            abs_url = urlparse.urljoin(response.url, rel_url.strip())
            if self.crawl_ruled(abs_url,
                                accept_netlocs=self.accept_netlocs,
                                regs_accept=self.regs_accept,
                                regs_reject=self.regs_reject):
                
                qprioirty = 100
                if utility.is66kJobDetail(abs_url) == True: # the blog post html is the highest priority
                    qprioirty = 400
                    yield Request(abs_url,priority=qprioirty)

                    
        if 'text/html' in response.headers['Content-Type']  :
            item = RawItem()

#             if(settings.USE_SELENIUM == True):
#                 item['raw_html'] =  self.getContentSelenium(response.url)
#             else: 
            item["raw_html"] = response.body
                
            item["url"] = response.url
            item['domain'] = self.name
            # pass to local file pipeline
            yield item
            
    """
    Pure function that applies a set of rules to a url to determine if it should
    be crawled. Returns True if it should be crawled.

    """
    @staticmethod
    def crawl_ruled(url, accept_netlocs=None, regs_accept=None,
                    regs_reject=None):
        # If None is supplied to netlocs, ignore accept_netlocs
        # If an empty list [] is supplied, returns False
        if accept_netlocs is not None:
            parts = urlparse.urlparse(url)
            now_domain = parts.netloc.lower()
            domain_parts = now_domain.split('.')
           
            for aurl in accept_netlocs :
                 accept_parts = aurl.split('.')
                 if len(domain_parts) == len(accept_parts) :
                    if aurl == now_domain :
                        return True
                    else:
                        return False
                 elif len(domain_parts) < len(accept_parts) :
                     return False
                 else:
                    for aa in accept_parts :
                        if aa not in domain_parts :
                            return False
                    return True
                    
#                 if parts.netloc.lower() not in accept_netlocs:
#                     return True
            return False

        if regs_accept is not None:
            accept = False
            for comp in regs_accept:
                if comp.search(url):
                    accept = True
            if accept is False:
                return False

        if regs_reject is not None:
            accept = True
            for comp in regs_reject:
                if comp.search(url):
                    accept = False
            if accept is False:
                return False

        return True
    @staticmethod
    def load_sitemap(sitemap):
        tree = xml.etree.ElementTree.parse(sitemap)
        root = tree.getroot()

        found_urls = []
        for url in root:
            if not url.tag.endswith('url'): continue
            for loc in url:
                if not loc.tag.endswith('loc'): continue
                found_urls.append(loc.text)
        return found_urls

    @staticmethod
    def urls_from_file(filename):
        f = open(filename, 'r')
        urls = [l.strip() for l in f]
        f.close()
        return urls

    def __init__(self, urls=None, sitemap=None, mirror=None, reg_accept=None,
                 reg_reject=None, domains=None, url_file=None):
        
        # initial remote browser
#         self.sel = selenium("localhost", 4444, "*firefox","http://www.pixnet.net")

        
        # Check the local folder is exit

#         if not os.path.exists(self.webpage_directory):
#             os.makedirs(self.webpage_directory)
        
        self.start_urls = []
        self.accept_netlocs = [] # By default, do not crawl links
        self.regs_accept = None
        self.regs_reject = None

        if urls is not None:
            urls = urls.split(',')
            self.start_urls.extend(urls)
        if url_file is not None:
            self.start_urls.extend(self.urls_from_file(url_file))
        if sitemap is not None:
            self.log("Sitemap crawl: %s" % sitemap, log.DEBUG)
            urls = self.load_sitemap(sitemap)
            self.start_urls.extend(urls)
        if reg_accept is not None:
            regs = reg_accept.split(',')
            self.regs_accept = [re.compile(reg) for reg in regs]
            self.accept_netlocs = None
                             # Setting accept_netlocs to None tells it to crawl
                             # accept any domain and links based on regexp
                             # unless domains or mirros is specified to override
        if reg_reject is not None:
            regs = reg_reject.split(',')
            self.regs_reject = [re.compile(reg) for reg in regs]
        if mirror is not None:
            parts = urlparse.urlparse(urls[0])
            self.accept_netlocs = [parts.netloc.lower()]
        # domains overrides mirror
        if domains is not None:
            domains = domains.split(',')
            self.accept_netlocs = domains

        if self.accept_netlocs:
            self.accept_netlocs = [n.lower() for n in self.accept_netlocs]
            self.log("Using accept_netlocs: %s" %self.accept_netlocs, log.DEBUG)
        if len(self.start_urls) > 5:
            self.log("Crawling many urls: %d" % len(self.start_urls), log.DEBUG)
        else:
            self.log("Crawling start_urls: %s" % self.start_urls, log.DEBUG)

            