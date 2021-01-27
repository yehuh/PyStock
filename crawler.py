from datetime import datetime, timedelta
#import urllib2, logging, csv, re
import requests
from io import StringIO
import pandas# as pd
import numpy as np

daterange = datetime.today()

# 下載股價
days_ago = [15]
worked_day = [10]

days_ago = np.array([datetime.today() - timedelta(days =i) for i in range(30)]) 

worked_day = np.array([datetime.today() - timedelta(days =i) for i in range(10)])

j= 0
for i in range(30):
    if(days_ago[i].weekday() <5):
        #print(days_ago[i])
        if(j<10):
            worked_day[j] = days_ago[i]
        
        j = j+1
        
for i in range(10):
    print(worked_day[i].strftime("%Y%m%d"))

        
#for i in range(5):
r = np.array([requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + worked_day[i].strftime("%Y%m%d") + '&type=ALL') for i in range(5)])    
    # 整理資料，變成表格
df = np.array([pandas.read_csv(StringIO(r[i].text.replace("=", "")),header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1) for i in range(5)])

#print(df.columns)
for i in range(5):
    print("              ")
    print("-------------")
    print('Date :'+ worked_day[i].strftime("%Y%m%d"))
    print(df[i].head(3))
    print("-------------")
    print("              ")
#print('Date :'+ worked_day[1].strftime("%Y%m%d"))
#print(df[1].head(3))

#stock_cnt = df.iloc['成交股數']

#print(df[0].成交股數)


# 顯示出來
#