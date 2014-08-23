# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.selector import HtmlXPathSelector

from jobcrawler import utility 

class InsideJobList(object):
    def process_item(self, item, spider):
        
        if utility.isInsideJobList(item['url']) == True :
            hxs = HtmlXPathSelector(item)
            anchors = hxs.select('//a/@href').extract()
            
            urls = hxs.select('//li[@class="job"]//a/@href').extract()
            titles = hxs.select('//li[@class="job"]//h3').extract()
            companys = hxs.select('//li[@class="job"]//span[@class="company"]/text()').extract()
            
            total = hxs.select('//div[@id="navigation"]/h2/span/text()').extract()
            r = re.search(r'[0-9]+',total[0] + '')
            total = r.group(0)
        
        return item
    
    
class InsideJobDetail(object):
    def process_item(self, item, spider):
        if utility.isInsideJobDetail(item['url']) == True :
            pass
        return item