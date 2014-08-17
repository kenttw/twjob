# -*- coding: utf-8 -*-
'''
Created on 2014年8月18日

@author: kent
'''
import scrapy

class InsideSpider(scrapy.Spider):
    name = "inside"
#     allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://jobs.inside.com.tw/",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)