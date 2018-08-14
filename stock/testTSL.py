
"""
Created on Sat Mar 31 13:44:05 2018

@author: lengfeiyan
"""
from urllib.request import urlopen, Request
import sys
sys.path.insert(0, 'C:\Program Files\Tinysoft\Analyse.NET')
import TSLPy3
#result = TSLPy3.DefaultConnectAndLogin('jyu')
stockInfo = TSLPy3.RemoteCallFunc("stock_realtime_data", ["SH600000"], {})

#data = stockInfo[1]
#dataLen = len(data) - 3
#for i in range(3,dataLen):
#    try:
#        print(data[i][3].decode('gbk'))
#        stock = data[i][3].decode('gbk').split(',')
#        message = stock[2][2:] + ',' + stock[3] + ',100'
#        print("http://47.100.100.244:3000/stock/publish?message=" + message)
#        req = Request("http://47.100.100.244:3000/stock/publish?message=" + message)
#        response = urlopen(req)
#        responseData = response.read()
#        print(responseData.decode('utf-8'))
#    except KeyError:
#        break
#print(stockInfo)
#
#for key in list(stockInfo[1][0].keys()):
#    print(key,',',key.decode('gbk'))

#TSLPy3.Disconnect()
