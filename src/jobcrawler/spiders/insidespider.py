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


class InsideSpider(scrapy.Spider):
    name = "InsideSpider"
#     allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://jobs.inside.com.tw/",
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
                if utility.isInsideJobList(abs_url) == True: # the blog post html is the highest priority
                    qprioirty = 400
                    yield Request(abs_url,priority=qprioirty)
                if utility.isInsideJobDetail(abs_url) == True:
                    yield Request(abs_url,priority=qprioirty)
                    
        if response.headers['Content-Type'] == 'text/html' :
            item = RawItem()

#             if(settings.USE_SELENIUM == True):
#                 item['raw_html'] =  self.getContentSelenium(response.url)
#             else: 
            item["raw_html"] = response.body
                
            item["url"] = response.url
            item['domain'] = self.name
            # pass to local file pipeline
            yield item
            