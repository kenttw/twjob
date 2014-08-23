# -*- coding: utf-8 -*-
'''
Created on 2014年8月18日

@author: kent
'''

import re

r = re.search(r'[0-9]+','中http222')
print r.group(0)