from datetime import datetime, timedelta
#import urllib2, logging, csv, re
import requests
from io import StringIO
import pandas# as pd
import numpy as np

#找出股市工作日期
daterange = datetime.today()

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


# 下載股價	
r=[]
for i in range(4):
	r.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + worked_day[i+1].strftime("%Y%m%d") + '&type=ALL'))
   
# 整理資料，變成表格
df =[]
for i in range(3):
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

for i in range(2):
	print("              ")
	print("-------------")
	print(deal_cnt[i+1])
	print("              ")

deal_cnt_3day = deal_cnt[1]
#deal_cnt_3day.iloc[:,2] = deal_cnt_3day.iloc[:,2] + deal_cnt[2].iloc[:,2]

print("-------------")
print("deal cnt 3day")
print(deal_cnt_3day)
print("              ")




#for i in range(1, 2):
#	deal_cnt_3day.iloc[:,2] = deal_cnt[i].iloc[:,2]+deal_cnt_3day.iloc[:,2]



