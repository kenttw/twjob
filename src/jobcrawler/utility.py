# -*- coding: utf-8 -*-
'''
Created on 2014年8月23日

@author: kent
'''
import re

ispaging = re.compile(r'^http://jobs\.inside\.com\.tw/jobs/page/[\d]+')
ishome = re.compile(r'^http://jobs\.inside\.com\.tw^')
isdetail = re.compile(r'http://jobs\.inside\.com\.tw/jobs/[\d]+')

def isInsideJobList(url):
    if ispaging.match(url) != None :
        return True;
    if ishome.match(url) != None :
        return True
    
    return False

def isInsideJobDetail(url):
    if isdetail.match(url) != None :
        return True
    return False