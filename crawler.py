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

################################找出股市工作日期################################
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
''################################找出股市工作日期################################

roc_year = int(real_work_day[0].year) - 1911
print("Year of ROC Now:")
print(str(roc_year))


#下載股價
DaysToCalc = 1
r=[]

whaha = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year)
whaha+='/'
whaha+=real_work_day[0].strftime("%m/%d")
whaha+='&s=0,asc,0'

print(whaha)

market_stock = []
market_stock.append(real_work_day[0].max)
for i in range(DaysToCalc):
    r.append(requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year) + '/' + real_work_day[i].strftime("%m/%d") + '&s=0,asc,0'))
	#r.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i].strftime("%Y%m%d") + '&type=ALL'))



                                                                                                                                #110/05/21&s=0,asc,0
# 整理資料，變成表格
#df =[]
#for i in range(DaysToCalc):
#    df.append(pd.read_csv(StringIO(r[i].text, header=["代號" in l for l in r[i].text.split("\n")].index(True)-1)))
    #df.append(pd.read_csv(StringIO(r[i].text.replace("=", "")), header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1))
   
k = r[0].text.split("\n")

df = pd.read_csv(r[0].text,header = ["代號" in l for l in r[0].text.split("\n")].index(True)-1)
print("                   ")
print("counter stock today")
print(df)
print("                   ")
print("                   ")
print("counter stock today above")


#df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)

#讀取證券代號
f = open('counter_stock_index.jn')
counter_stock = json.load(f)
#print(data[0])

f =open('market_stock_index.json')
market_stock = json.load(f)
for i in range(len(counter_stock)):
    market_stock.append(counter_stock[i])

print("----------------------")
print("Count of Stock in Taiwan")
print(len(market_stock))
print("                   ")
print("                   ")



#################找出證券代號中對應的成交量並存於 deal_cnt_per_day#################
deal_cnt_per_day = []

#print("len of df")
#print(len(df[0].index))
#print("                 ")

#print("len of market_stock")
#print(len(market_stock))
#print("                 ")
start_pos = 0
for k in range(DaysToCalc):
    deal_cnt =[]
    stock_no =[]
    if(df[k]is None):
        print("dataframe on line not exist")
        print("-------------------")
        continue
    #########df的證券代號與 market_stock 比對後加入#########
    for i in range(int(len(market_stock))):
        if(market_stock[i] is None):
            continue
        for j in range(start_pos, len(df[k].index)):
            if(df[k].iloc[j,0] is None):
                print("dataframe not exist")
                print("-------------------")
                continue
            if (market_stock[i] == df[k].iloc[j,0]):
                stock_no.append(market_stock[i])
                d_c_temp = str(df[k].iloc[j,2]).replace(",", "")
                deal_cnt.append(int(d_c_temp))
                #print("-----------------------------------")
                #print(market_stock[i]+" stock added")
                #print("deal count = " + d_c_temp)
                #print("-----------------------------------")
                #print("                                   ")
                
                #df的證券代號與 market_stock 為一對一且順序皆為由小到大
                #=>下個證券代號從現在的位置找起
                start_pos = j 
                break;
    start_pos = 0
    df_data = {"證券代號":stock_no, "成交股數":deal_cnt}
    df_temp = pd.DataFrame(df_data)
    deal_cnt_per_day.append(df_temp)
    #
    #########df的證券代號與market_stock 比對後加入#########
    
#print("deal count 1st day = ")    
#print(deal_cnt_per_day[0].head(10))

##
#################找出證券代號中對應的成交量並存於 deal_cnt_per_day#################



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
    
#deal_cnt_3day = pd.DataFrame(columns=("證券代號","成交股數"))

#print(deal_cnt_3day)
import copy
total_deal_cnt = copy.copy(deal_cnt_per_day[0])

deal_cnt_per_stock = []

for day in range(DaysToCalc):
    print("stock cnt in day"+ str(day))
    print(len(deal_cnt_per_day[day].index))

stock_row =[]
for day in range(1,DaysToCalc):
    print("###################")
    print("                   ")
    print("day :"+str(day))
    print("                   ")
    print("###################")
    print("                   ")
    print("                   ")
    for stock_index in deal_cnt_per_day[day].index:
        #print("-------------------")
        #print(deal_cnt_per_day[day].loc[stock_index,["證券代號"]])
        #print("                   ")
        #print(deal_cnt_per_day[day].loc[stock_index,["成交股數"]])
        #print("                   ")
        stock_to_found = deal_cnt_per_day[day].loc[stock_index,["證券代號"]]
        for tdc_index in total_deal_cnt.index:
            stock_compare_to = total_deal_cnt.loc[tdc_index,["證券代號"]]
            if(str(stock_to_found) == str(stock_compare_to)):
                buff = total_deal_cnt.loc[tdc_index,["成交股數"]] + deal_cnt_per_day[day].loc[stock_index,["成交股數"]]
                total_deal_cnt.loc[tdc_index,["成交股數"]] = buff
                #print("證券代號 " + total_deal_cnt.loc[tdc_index,["證券代號"]])
                #print("加入")                               
                break
        #for day in range(days_to_calc):
        #    print("證券代號 = ")
        #    print(deal_cnt_per_day[day].loc[stock_index,["證券代號"]])
        #    buff = buff+deal_cnt_per_day[day].loc[stock_index,["成交股數"]]
        #row_data = {"證券代號": [deal_cnt_per_day[day].loc[stock_index,["證券代號"]]], "成交股數":[buff]}
        #stock_row.append(row_data)

#total_deal_cnt_for_days_to_calc = pd.DataFrame(stock_row, columns=["證券代號","成交股數"])    

end_time = time.time()
print("-------------")
print("calculating time is")
print(end_time - start_time)

print("Stock Cnt For Total Deal Count:")
print(len(total_deal_cnt.index))

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



deal_cnt_over_deal =[]
stock_no_over_deal =[]

for stock_index in total_deal_cnt.index:
    deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["成交股數"]])
    deal_cnt_today = int(deal_cnt_per_day[0].loc[stock_index,["成交股數"]])
    if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
        deal_cnt_over_deal.append(deal_cnt_today)
        stock_no_over_deal.append(deal_cnt_per_day[0].loc[stock_index,["證券代號"]])
over_deal_data = {"證券代號":stock_no_over_deal, "成交股數":deal_cnt_over_deal}
OverDealDf = pd.DataFrame(over_deal_data)

#for day in range(DaysToCalc):
print("-------------")
print("deal cnt Day 0")
print(deal_cnt_per_day[day].head(50))
print("             ")
    

str_buff = "deal cnt sum for " + str(DaysToCalc)
str_buff = str_buff + " days:"
print("-------------")
print(str_buff)
print(total_deal_cnt.head(50))
#print(total_deal_cnt.loc["成交股數"])#[1]deal_cnt_3day
print("              ")
print("              ")

print("-------------")
print("over deal stock")
print(OverDealDf)

#for i in range(1, 2):
#	deal_cnt_3day.iloc[:,2] = deal_cnt[i].iloc[:,2]+deal_cnt_3day.iloc[:,2]
