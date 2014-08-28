# -*- coding: utf-8 -*-

# Scrapy settings for jobcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jobcrawler'

SPIDER_MODULES = ['jobcrawler.spiders']
NEWSPIDER_MODULE = 'jobcrawler.spiders'

########### Item pipeline
ITEM_PIPELINES = {
                  "jobcrawler.pipelines.InsideJobList": 10 , 
                  "jobcrawler.pipelines.InsideJobDetail": 30 , 
}

HADOOP_HOST = '210.63.38.209'
HBASE_PORT ='9191'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jobcrawler (+http://www.yourdomain.com)'
