# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 20:42:26 2018

@author: lengf
"""

from urllib.request import urlopen, Request


req = Request("http://47.100.100.244:3000/stock/publish?message=600050,5,100")
response = urlopen(req)
data = response.read()
print(data)