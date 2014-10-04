# -*- coding: utf-8 -*-
'''
Created on 2014年8月23日

@author: kent
'''
import re
import unittest


ispaging = re.compile(r'^http://jobs\.inside\.com\.tw/jobs/page/[\d]+')
ishome = re.compile(r'^http://jobs\.inside\.com\.tw^')
isdetail = re.compile(r'http://jobs\.inside\.com\.tw/jobs/[\d]+')

# http://66kjobs.tw/jobs/329
job66kDetail = re.compile(r'^http://66kjobs\.tw/jobs/[\d]+$')

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

def is66kJobDetail(url):
    if job66kDetail.match(url) != None :
        return True
    return False


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass # do not thing
    
    def test_regularExpressList(self):
        self.assertEqual(is66kJobDetail('http://66kjobs.tw/jobs/32aaaa9') ,False , 'can;t dectect wrong url')
        self.assert_(is66kJobDetail('http://66kjobs.tw/jobs/33333'), 'cant detect right url')
        

# if __name__ == '__main__':
#     unittest.main()