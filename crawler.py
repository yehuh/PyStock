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
r = np.array([requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + worked_day[i].strftime("%Y%m%d") + '&type=ALL') for i in range(4)])
    
    # 整理資料，變成表格
df =[]
for i in range(4):
	df.append(pandas.read_csv(StringIO(r[i].text.replace("=", "")), header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1))

for i in range(3):
    print("              ")
    print("-------------")
    print('Date :'+ worked_day[i].strftime("%Y%m%d"))
    print(df[i].head(3))
    print("-------------")
    print("              ")

deal_cnt_frame = []
for i in range(3):
	deal_cnt_frame.append(df[i].iloc[:,[0,2]])
	
print(deal_cnt_frame[0].tail(5))
print(deal_cnt_frame[1].tail(5))
print(deal_cnt_frame[2].tail(5))


deal_cnt = []
for i in range(3):
	deal_cnt.append(deal_cnt_frame[i].tail(5))

for i in range(3):
	print("              ")
	print("-------------")
	print(deal_cnt[i])
	print("              ")

#deal_cnt_3day = deal_cnt[0]

#for i in range(1, 2):
#	deal_cnt_3day.iloc[:,2] = deal_cnt[i].iloc[:,2]+deal_cnt_3day.iloc[:,2]

#print(deal_cnt_3day) #.tail(5)

