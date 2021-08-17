from datetime import datetime, timedelta, date
#import urllib2, logging, csv, re
import requests
from io import StringIO
import pandas as pd
#import DataFrameToJSONArray
import json
import GetWorkedDay


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

real_work_day = GetWorkedDay.GetWorkedDay(80)

roc_year = int(real_work_day[0].year) - 1911
print("Year of ROC Now:")
print(str(roc_year))


whaha = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year)
whaha+='/'
whaha+=real_work_day[0].strftime("%m/%d")
whaha+='&s=0,asc,0'

print(whaha)

#market_stock = []
#market_stock.append(real_work_day[0].max)


#下載股價
DaysToCalc = 7
r_counter=[]
r_market=[]
for i in range(DaysToCalc):
    r_counter.append(requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year) + '/' + real_work_day[i].strftime("%m/%d") + '&s=0,asc,0'))
    r_market.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i].strftime("%Y%m%d") + '&type=ALL'))



                                                                                                                      
############################################################整理上市股票資料，變成表格############################################################
df_market =[]
for i in range(DaysToCalc):
    df_buff = pd.read_csv(StringIO(r_market[i].text.replace("=", "")), header=["證券代號" in l for l in r_market[i].text.split("\n")].index(True)-1)
    #"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"
    df_buff1 = df_buff.drop(columns=["證券名稱","成交筆數","成交金額","開盤價","最高價","最低價","收盤價"])
    df_buff2 = df_buff1.drop(columns=["最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"])
    df_buff2 = df_buff2.drop(columns=["漲跌(+/-)","Unnamed: 16"])
    columns_titles = ["證券代號","漲跌價差","成交股數"]
    df_buff2=df_buff2.reindex(columns=columns_titles)
    df_buff3 = df_buff2.rename(columns = {"證券代號": "代號", "漲跌價差": "漲跌"}, inplace = False)
    #for j in df_buff2.index:
    #    buff = str(df_buff2.loc[j,["漲跌(+/-)"]])
    #    buff2 = buff+str(df_buff2.loc[j,["漲跌價差"]])
    #    df_buff2.loc[j,["漲跌價差"]] = buff2
    df_market.append(df_buff3)
'' ############################################################整理上市股票資料，變成表格############################################################

#df = pd.read_csv(r[0].text, header = None)
print("                   ")
print("market stock today colum name")
print(df_market[0])
#print(df_buff2.columns[2])
#print(df_buff2.columns[3])
print("                   ")
print("                   ")
print("market stock today above")


############################################################整理上櫃股票資料，變成表格############################################################
couter_stock_data =[]
df_counter =[]
for idd in range(DaysToCalc):
    k = r_counter[idd].text.split("\n")
    index_line = 0
    for i in range(len(k)):
        if(k[i].find("代號")!=-1):
            index_line = i
            break
    
    for i in range(index_line):
        k.pop(0)
    
    stock_data_index = k[0].split(",")
    #print("                   ")
    #print("dataframe index" + str(idd))
    #print(stock_data_index)
    #print("                   ")

    index_str = ""
    for l in stock_data_index:
        buffd = '\"' + l.strip()
        buffd = buffd+ '\"'
        buffd = buffd+ ','
        index_str += buffd
    
    index_str = index_str.rstrip(',')

    k.pop(0)
    k.insert(0,index_str)

    couter_stock_data.append("")
    for data_str in k:
        couter_stock_data[-1] += data_str
        couter_stock_data[-1] +='\n'

    couter_stock_data[-1] = couter_stock_data[-1].strip()
    df_buff = pd.read_csv(StringIO(couter_stock_data[-1]),header=0)
    df_buff1 = df_buff.drop(columns=["名稱", "收盤", "開盤", "最高", "最低", "成交筆數","最後買價", "最後買量(千股)"])
    df_buff2= df_buff1.drop(columns=["最後賣價","最後賣量(千股)","發行股數" ,"次日參考價" , "次日漲停價"])
    df_buff2 = df_buff2.drop(columns=["均價","成交金額(元)","次日跌停價"])#,"次日跌停價\r" 
    df_counter.append(df_buff2)
'' ############################################################整理上櫃股票資料，變成表格############################################################

#df = pd.read_csv(r[0].text, header = None)
print("                   ")
print("counter stock today colum name")
print(df_counter[0])
#print(df_buff.columns[1])
#print(df_buff.columns[2])
print("                   ")
print("                   ")
print("counter stock today above")

#dfts = DataFrameToJSONArray(df_buff2, 'OverDealCntCounter.json') # 引數(df資料,檔案儲存路徑)
#dfts.funChangeDataFrameType() # 自動轉換DataFrame的列資料型別
#dfts.funSaveJSONArrayFile() # 儲存JSON格式檔案
#df_buff2.to_json(r'OverDealCntCounter.json')

#df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)

df =[]
for dayk in range(DaysToCalc):
    df.append(pd.concat([df_market[dayk], df_counter[dayk]], ignore_index=True))

print("                   ")
print("modified counter stock today ")
print(df[0])
#print(df_buff.columns[1])
#print(df_buff.columns[2])
print("                   ")
print("                   ")
print("counter stock today above")


#讀取證券代號
f = open('counter_stock_index.json')
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
    print("len of df")
    print(len(df[k].index))
    print("                 ")
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
        for j in range(start_pos,len(df[k].index)):  #,
            #print("-------------")    
            #print("counter no =")
            #buff0 = df[k].iloc[j,:]
            #buff1 = buff0.loc["代號"]
            #print(buff0)
            #print("              ")
            if(df[k].iloc[j,0] is None):
                print("dataframe not exist")
                print("-------------------")
                continue
            if (market_stock[i] == df[k].iloc[j,0]):
                stock_no.append(market_stock[i])
                d_c_temp = str(df[k].iloc[j,2]).replace(",", "")
                #print("-----------------------------------")
                #print(counter_stock[i]+" stock added")
                #print("deal count = ")
                #print(d_c_temp)
                #print("-----------------------------------")
                #print("                                   ")
                deal_cnt.append(int(d_c_temp))
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


''#################找出證券代號中對應的成交量並存於 deal_cnt_per_day#################




##################################個別股票的交易量加總##################################
import copy
total_deal_cnt = copy.copy(deal_cnt_per_day[0])

for day in range(DaysToCalc): 
    print("stock cnt in day"+ str(day))
    print(len(deal_cnt_per_day[day].index))

stock_row =[]
start_pos = 0
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
        for tdc_index in range(start_pos ,len(total_deal_cnt.index)):
            stock_compare_to = total_deal_cnt.loc[tdc_index,["證券代號"]]
            if(str(stock_to_found) == str(stock_compare_to)):
                buff = total_deal_cnt.loc[tdc_index,["成交股數"]] + deal_cnt_per_day[day].loc[stock_index,["成交股數"]]
                total_deal_cnt.loc[tdc_index,["成交股數"]] = buff
                #print("證券代號 " + total_deal_cnt.loc[tdc_index,["證券代號"]])
                #print("加入")
                start_pos = tdc_index
                break
    start_pos = 0;
        #for day in range(days_to_calc):
        #    print("證券代號 = ")
        #    print(deal_cnt_per_day[day].loc[stock_index,["證券代號"]])
        #    buff = buff+deal_cnt_per_day[day].loc[stock_index,["成交股數"]]
        #row_data = {"證券代號": [deal_cnt_per_day[day].loc[stock_index,["證券代號"]]], "成交股數":[buff]}
        #stock_row.append(row_data)

#total_deal_cnt_for_days_to_calc = pd.DataFrame(stock_row, columns=["證券代號","成交股數"])    
'' ##################################個別股票的交易量加總##################################


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


######################################找今天交易量大於前幾天總和的股票######################################
deal_cnt_over_deal =[]
stock_no_over_deal =[]

for stock_index in total_deal_cnt.index:
    deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["成交股數"]])
    deal_cnt_today = int(deal_cnt_per_day[0].loc[stock_index,["成交股數"]])
    if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
        deal_cnt_over_deal.append(deal_cnt_today)
        stock_no_over_deal.append(deal_cnt_per_day[0].iloc[stock_index,0])
        
over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal}
OverDealDf = pd.DataFrame(over_deal_data)
''######################################找今天交易量大於前幾天總和的股票######################################


file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"OverDealStocks.json"
OverDealDf.to_json(file_name_str, orient='records')
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


######################################找今天交易量大於前幾天總和10倍的股票######################################
#start_pos =0
#deal_cnt_extrem_over_deal=[]
#stock_no_extrem_over_deal=[]
#for over_deal_index in OverDealDf.index:
#    for index_today in  range(start_pos,len(deal_cnt_per_day[0].index)):
#        if(OverDealDf.iloc[over_deal_index,0] == deal_cnt_per_day[0].iloc[index_today,0]):
#            start_pos = index_today
#            deal_cnt_today = int(deal_cnt_per_day[0].iloc[index_today,1])
#            deal_cnt_sum = int(OverDealDf.iloc[over_deal_index,1])
#            if(deal_cnt_today> 10*deal_cnt_sum):
#                deal_cnt_extrem_over_deal.append(deal_cnt_today)
#                stock_no_extrem_over_deal.append(OverDealDf.iloc[over_deal_index,0])
#            break;


#extreme_over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal}
#ExOverDealDf = pd.DataFrame(extreme_over_deal_data)

#print("-------------")
#print("extreme over deal stock")
#print(ExOverDealDf)
''######################################找今天交易量大於前幾天總和10倍的股票######################################