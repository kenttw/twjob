# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
import happybase
from jobcrawler import utility , settings

class Job66KDetail(object) :
    def process_item(self, item, spider) :
        if utility.is66kJobDetail(item['url']) :
            
            hxs = Selector(text=item['raw_html'])
            
            # //*/div[@class="job-content"]/h2/text() >>> job title
            item['jobtitle'] = hxs.xpath('//*/div[@class="job-content"]/h2/text()').extract()[0].encode('utf-8')
            
            # //*/div[@class="job-content"]/h2/a[1]/text() >>> company name
            try :
                item['companyName'] = hxs.xpath('//*/div[@class="job-content"]/h2/a[1]/text()').extract()[0].encode('utf-8')
            except IndexError as e :
                pass
            
            # //*/div[@class="job-content"]/h2/a/@href >>> company url
            try : 
                item['companyUrl'] = hxs.xpath('//*/div[@class="job-content"]/h2/a/@href').extract()[0].encode('utf-8')
            except IndexError as e :
                pass
            
            # //*/div[@class="job-desc"] >>> job description
            item['jobdetial'] = hxs.xpath('//*/div[@class="job-desc"]').extract()[0].encode('utf-8')
            
            # //*/div[@class="well"] >>> apply method
            item['applyMethod'] = hxs.xpath('//*/div[@class="well"]').extract()[0].encode('utf-8')
            
#             for key , value in item.items():  # get meta terms at pixTerm
#                 print 'key=%s , value=%s' % (key , value)
            toHbase(item)

            return item

class InsideJobList(object):
    def process_item(self, item, spider):
        
        if utility.isInsideJobList(item['url']) == True :
            hxs = Selector(text=item['raw_html'])
#             hxs = HtmlXPathSelector(item['raw_html']+'')
#             anchors = hxs.select('//a/@href').extract()
            
#             urls = hxs.xpath('//li[@class="job"]//a/@href').extract()
            url = item['url']
            titles = hxs.xpath('//li[@class="job"]//h3').extract()
            companys = hxs.xpath('//li[@class="job"]//span[@class="company"]/text()').extract()[0]
            
            total = hxs.select('//div[@id="navigation"]/h2/span/text()').extract()[0]
            r = re.search(r'[0-9]+', total[0] + '')
            total = r.group(0)
        
        return item
    
    
class InsideJobDetail(object):
    
#     mm = re.compile(r'^[\d].*[\d]$+',re.UNICODE)
    def process_item(self, item, spider):
        if utility.isInsideJobDetail(item['url']) == True :
#             print item['url']


#             data = {}
#             item['url']
            
            hxs = Selector(text=item['raw_html'])
            category = hxs.xpath(r'//*[@id="main-content"]/div[3]/h1/span[1]/text()').extract()[0]
            category = category[category.index(u'：') + 1:]
            item['category'] = category.encode('utf-8')
            
            
            money = hxs.xpath(r'//*[@id="main-content"]/div[3]/h1/span[2]/text()').extract()[0]
            money = money[money.index(u'：') + 1:]
            item['money'] = money.encode('utf-8')
            
            if u'，' in money :
                ymoney = money[money.index(u'，') + 1:]
                mmoney = money[:money.index(u'，') - 1]
                print ymoney , mmoney.encode('utf-8')
            
            print category , money
            
            location = hxs.xpath(r'//span[@class="location"]/text()').extract()[0]
            item['location'] = location.encode('utf-8')
            
            date = hxs.xpath(r'//span[@class="date"]/text()').extract()[0]
            item['date'] = date.encode('utf-8')
            
            jobdetial = hxs.xpath(r'//*[@id="job-info"]/text()').extract()[0]
            item['jobdetial'] = jobdetial.encode('utf-8')
            
            toHbase(item)
            
#             pass
        return item
    
def toHbase(item):
# TODO: write to hbase 
# TODO: get table from global parameter
        try:
#             if etutility.isPixNetBlog(item['url']) == True:
#                 pixItem = self.localFile.extract_pixItem_fromRaw(item) 
                connection = happybase.Connection(settings.HADOOP_HOST, settings.HBASE_PORT)
                table = connection.table('goodjob')
#                 rowKey = pixItem.genRowKey()
        #         table.put(rowKey, {'f:qual1': 'value1'})
                writedta = {}
#                 data['f1:test'] = 'hello'
                for key , value in item.items():  # get meta terms at pixTerm
                    writedta['f:' + key] = value
                table.put(item['url'] , writedta)
#                 print "write to hbase ok "
        except Exception as e:
            print e
    
class DocumentToHBase(object):
    
    
    def __init__(self):
        pass
#         localFile = LocalFile()
    
    def process_item(self, item):
# TODO: write to hbase 
# TODO: get table from global parameter
        try:
#             if etutility.isPixNetBlog(item['url']) == True:
#                 pixItem = self.localFile.extract_pixItem_fromRaw(item) 
                connection = happybase.Connection(settings.HADOOP_HOST, settings.HBASE_PORT)
                table = connection.table('goodjob')
#                 rowKey = pixItem.genRowKey()
        #         table.put(rowKey, {'f:qual1': 'value1'})
                data = {}
#                 data['f1:test'] = 'hello'
                for key , value in item.items():  # get meta terms at pixTerm
                    data['f1:' + key] = value
                table.put(item['url'] , data)
#                 print "write to hbase ok "
        except Exception as e:
            print e
