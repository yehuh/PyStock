from datetime import datetime, timedelta, date
#import urllib2, logging, csv, re
import requests
from io import StringIO
import pandas as pd
import numpy as np
from copy import deepcopy

#設定2021的假日
holidays_taiwan_2021 = []
holidays_taiwan_2021.append(date(2021, 1, 1))
holidays_taiwan_2021.append(date(2021, 2, 10))
holidays_taiwan_2021.append(date(2021, 2, 11))
holidays_taiwan_2021.append(date(2021, 2, 12))
holidays_taiwan_2021.append(date(2021, 2, 15))
holidays_taiwan_2021.append(date(2021, 2, 16))
holidays_taiwan_2021.append(date(2021, 3, 1))
holidays_taiwan_2021.append(date(2021, 4, 2))
holidays_taiwan_2021.append(date(2021, 4, 5))
holidays_taiwan_2021.append(date(2021, 4, 30))
holidays_taiwan_2021.append(date(2021, 6, 14))
holidays_taiwan_2021.append(date(2021, 9, 20))
holidays_taiwan_2021.append(date(2021, 9, 21))
holidays_taiwan_2021.append(date(2021, 10, 11))
holidays_taiwan_2021.append(date(2021, 12, 31))

'''
for day in holidays_taiwan_2021:
	print(day.strftime("%Y%m%d"))
	print("week day is %d" % day.weekday())
	print("                               ")
'''

all_stock = pd.read_html("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2", match ="有價證券代號及名稱")
print(len(all_stock))
df = all_stock[0]
print(df.loc[df["0"]=="上市認購(售)權證"])


#設定台股代號
stock_code = []
stock_code.append("1101")
stock_code.append("1102")
stock_code.append("1103")
stock_code.append("1104")
stock_code.append("1108")
stock_code.append("1109")
stock_code.append("1109")
stock_code.append("1110")
stock_code.append("1201")
stock_code.append("1203")
stock_code.append("1210")
stock_code.append("1213")

#找出股市工作日期
'''
days_ago = []
for i in range(80):
	days_ago.append(datetime.today() - timedelta(days = i))
# = np.array([datetime.today() - timedelta(days =i) for i in range(60)]) 

worked_day = []
real_work_day =[]
#np.array([datetime.today() - timedelta(days =i) for i in range(60)])

#print(days_ago[i])
j= 0

for dayyy in days_ago:
	if dayyy.weekday() < 5:
		worked_day.append(dayyy)

#for i in range(60):
#	if days_ago[i].weekday() <5:
#		worked_day.append(days_ago[i])
        		
				#break
				#

for dayy in worked_day:
	was_holiday = False
	for holiday in holidays_taiwan_2021:
		if dayy.date() == holiday:
			was_holiday = True
			break
	if was_holiday == False:
		real_work_day.append(dayy)

        
#for day in real_work_day:
#	print(day.strftime("%Y%m%d"))


# 下載股價


r=[]
for i in range(1,4):
	r.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i].strftime("%Y%m%d") + '&type=ALL'))
   
# 整理資料，變成表格
df =[]
for i in range(3):
	df.append(pd.read_csv(StringIO(r[i].text.replace("=", "")), header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1))




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
	
print(deal_cnt_frame[0].head(5))
print(deal_cnt_frame[1].head(5))
print(deal_cnt_frame[2].head(5))



deal_cnt = []
for i in range(3):
	deal_cnt.append(deal_cnt_frame[i])

for i in range(2):
	print("              ")
	print("-------------")
	print("Date:"+real_work_day[i].strftime("%Y%m%d"))
	print(deal_cnt[i].loc[deal_cnt[i]["證券代號"]==stock_code[0]])
	print(deal_cnt[i].loc[deal_cnt[i]["證券代號"]==stock_code[1]])

'''
#stock = []
#stock.append({"證券代號":["0050","0051","0052"], "成交股數":[11,22,33]})
#stock.append({"證券代號":["0050","0051","0052"], "成交股數":[44,55,66]})

#deal_cnt = []
#deal_cnt.append(pd.DataFrame.from_dict(stock[0]))
#deal_cnt.append(pd.DataFrame.from_dict(stock[1]))
'''

'''
'''
for i in range(3):
	buff = deal_cnt[i]["成交股數"].str.replace(",", "")#.astype(int)
	deal_cnt[i]["成交股數"] = buff.astype(int)
	
deal_cnt_3day = deal_cnt[0].copy()#.loc[deal_cnt[0]['成交股數']==specific_id,:].copy()

for i in range(2):
	deal_cnt_3day["成交股數"] = deal_cnt_3day["成交股數"]+deal_cnt[i+1]["成交股數"]

#buffj = []
#for i in range(3):
buffj = deal_cnt[0].iloc[:,[1]] + deal_cnt[1].iloc[:,[1]]

#deal_cnt_3day["成交股數"] = buffj.copy()

print("-------------")
print("deal cnt 1st day")
print(deal_cnt[0])
print("              ")
print("-------------")
print("deal cnt 2nd day")
print(deal_cnt[1])
print("              ")
print("-------------")
print("deal cnt 3rd day")
print(deal_cnt[2])
print("              ")
print("              ")
print("              ")
print("-------------")
print("deal cnt sum")
print(deal_cnt_3day)#[1]deal_cnt_3day
print(deal_cnt_3day.dtypes)#[1]deal_cnt_3day
print("              ")
'''


#for i in range(1, 2):
#	deal_cnt_3day.iloc[:,2] = deal_cnt[i].iloc[:,2]+deal_cnt_3day.iloc[:,2]
