# -*- coding: utf-8 -*-
'''
Created on 2014年8月24日

@author: kent
'''
import happybase
from jobcrawler import settings


class DocumentToHBase(object):
    
    
    def __init__(self):
        pass
#         localFile = LocalFile()
    
    def process_item(self):
# TODO: write to hbase 
# TODO: get table from global parameter
        try:
#             if etutility.isPixNetBlog(item['url']) == True:
#                 pixItem = self.localFile.extract_pixItem_fromRaw(item) 
                connection = happybase.Connection(settings.HADOOP_HOST,settings.HBASE_PORT)
                table = connection.table('goodjob')
#                 rowKey = pixItem.genRowKey()
        #         table.put(rowKey, {'f:qual1': 'value1'})
                data ={}
                data['f1:test'] = 'hello'
#                 for key , value in pixItem.items(): # get meta terms at pixTerm
#                     data['f:'+key] = value
                table.put('key1' , data)
                print "write to hbase ok "
        except Exception as e:
            print e

def main():
    d = DocumentToHBase()
    d.process_item()

if __name__ == '__main__':
    main()
    pass