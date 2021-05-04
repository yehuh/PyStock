from datetime import datetime, timedelta, date
#import urllib2, logging, csv, re
import requests
from io import StringIO
import pandas as pd
import json

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


#找出台股上市上櫃代號

#上櫃股票
#https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y

'''
counter_stock = pd.read_html("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y")
df_counter = counter_stock[0]
stock_names = df_counter.loc[:,2]

counter_stock_no =[]
for i in range(1, len(stock_names.index)):
	stock_str = stock_names.iloc[i].split()
	counter_stock_no.append(stock_str[0])


with open('counter_stock_index.json', 'w') as c_stock_id:
	json.dump(counter_stock_no, c_stock_id)

print('counter stockindex : ')
print(counter_stock_no)
'''

#上市股票
#https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y

'''
market_stock = pd.read_html("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y")
df_market = market_stock[0]
m_stock_names =df_market.loc[:,2]

market_stock_no =[]
for i in range(1, len(m_stock_names.index)):
	stock_str = m_stock_names.iloc[i].split()
	market_stock_no.append(stock_str[0])

with open('market_stock_index.json', 'w') as m_stock_id:
	json.dump(market_stock_no, m_stock_id)

print('stock_index : ')
print(market_stock_no)
'''
import time

start_time = time.time()

#找出股市工作日期

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
#    print(day.strftime("%Y%m%d"))

days_to_calc = 10
# 下載股價
r=[]
for i in range(days_to_calc):
	r.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i+1].strftime("%Y%m%d") + '&type=ALL'))
#r =(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[1].strftime("%Y%m%d") + '&type=ALL'))

# 整理資料，變成表格
df =[]
for i in range(days_to_calc):
    df.append(pd.read_csv(StringIO(r[i].text.replace("=", "")), header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1))

#df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)

#讀取證券代號
f = open('counter_stock_index.json')
counter_stock = json.load(f)
#print(data[0])

f =open('market_stock_index.json')
market_stock = json.load(f)


#找出證券代號中對應的成交量並存於 deal_cnt_frame_array
deal_cnt_frame_array = []


for k in range(days_to_calc):
    deal_cnt_frame =[]
    for i in range(int(len(market_stock)/2)):
        for j in range(len(df[0].index)):
            if (market_stock[i] == df[k].iloc[j,0]):
                deal_cnt_frame.append(df[k].iloc[j,[0,2]])
                break;
    deal_cnt_frame_array.append(deal_cnt_frame)
    


'''
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
#print("deal_cnt_frame_array[0].index")
#print(deal_cnt_frame_array[0][0]["成交股數"])

#將成交股數的型態換成int
for i in range(days_to_calc):
    for j in range(len(deal_cnt_frame_array[0])):
        buff = deal_cnt_frame_array[i][j]["成交股數"].replace(",", "")
        deal_cnt_frame_array[i][j]["成交股數"] = int(buff)#.astype(int)

    
#deal_cnt_3day = pd.DataFrame(columns=("證券代號","成交股數"))

#print(deal_cnt_3day)

stock_row =[]
for j in range(len(deal_cnt_frame_array[0])):
    buff =0
    for i in range(days_to_calc):
        buff = buff+int(deal_cnt_frame_array[i][j]["成交股數"])
    row_data = {"證券代號": [deal_cnt_frame_array[0][j]["證券代號"]], "成交股數":[buff]}
    stock_row.append(row_data)

deal_cnt_for_days_to_calc = pd.DataFrame(stock_row, columns=["證券代號","成交股數"])    

end_time = time.time()
print("-------------")
print("calculating time is")
print(end_time - start_time)

'''
print("-------------")
print("deal cnt 1st day")
print(deal_cnt_frame_array[0])
print("              ")
print("-------------")
print("deal cnt 2nd day")
print(deal_cnt_frame_array[1])
print("              ")
print("-------------")
print("deal cnt 3rd day")
print(deal_cnt_frame_array[2])
print("              ")
print("              ")
print("              ")
'''
print("-------------")
print("deal cnt sum")
print(deal_cnt_for_days_to_calc)
print(type(deal_cnt_for_days_to_calc))#[1]deal_cnt_3day
print("              ")



#for i in range(1, 2):
#	deal_cnt_3day.iloc[:,2] = deal_cnt[i].iloc[:,2]+deal_cnt_3day.iloc[:,2]
