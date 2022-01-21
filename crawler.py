import pandas as pd
#import urllib2, logging, csv, re
import requests
from io import StringIO
from datetime import datetime, timedelta, date, time

import time as tm
#import DataFrameToJSONArray
import json
import GetWorkedDay
import StockOnline


#找出台股上市上櫃代號
#stock_noooo = StockOnline.GetStockNo(StockOnline.eStockType.CONTER)

#import time

start_time = datetime.now()

real_work_day = GetWorkedDay.GetWorkedDay(80)

stock_closed_time = time(15,0,0)
work_day_shift = 0
if(date.today() ==  real_work_day[0].date()):
    print("today is work day")
    if(datetime.now().time() < stock_closed_time):
        print("Stock Dealing data of Today is not prepared")
        work_day_shift =1
else:
    print("today is not work day")

roc_year = int(real_work_day[0].year) - 1911
print("Year of ROC Now:")
print(str(roc_year))

#market_stock = []
#market_stock.append(real_work_day[0].max)



#下載股價
DaysToCalc = 7
r_counter=[]
r_market=[]
for i in range(DaysToCalc):
    roc_year_conter = int(real_work_day[i].year) - 1911
    r_counter.append(requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year_conter) + '/' + real_work_day[i+work_day_shift].strftime("%m/%d") + '&s=0,asc,0'))
    r_market.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i+work_day_shift].strftime("%Y%m%d") + '&type=ALL'))



                                                                                                                      
############################################################整理上市股票資料，變成表格############################################################
df_market =[]
for i in range(DaysToCalc):
    df_buff = pd.read_csv(StringIO(r_market[i].text.replace("=", "")), header=["證券代號" in l for l in r_market[i].text.split("\n")].index(True)-1)
    #"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"
    df_buff1 = df_buff.drop(columns=["證券名稱","成交筆數","成交金額","開盤價","最高價","最低價"])#,"收盤價"
    df_buff2 = df_buff1.drop(columns=["最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"])
    df_buff2 = df_buff2.drop(columns=["漲跌(+/-)","Unnamed: 16"])
    columns_titles = ["證券代號","漲跌價差","成交股數","收盤價"]
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
print("market stock today are listed above")


############################################################整理上櫃股票資料，變成表格############################################################
couter_stock_data =[]
df_counter =[]
disp_flag = 0
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
    df_buff2= df_buff1.drop(columns=["最後賣量(千股)","發行股數" ,"次日參考價" , "次日漲停價"])#"最後賣價",
    df_buff2 = df_buff2.drop(columns=["均價","成交金額(元)","次日跌停價"])#,"次日跌停價\r" 
    columns_titles = ["代號","漲跌","成交股數","最後賣價"]
    df_buff2=df_buff2.reindex(columns=columns_titles)
    df_buff3 = df_buff2.rename(columns = {"最後賣價": "收盤價"}, inplace = False)
    df_counter.append(df_buff3)
'' ############################################################整理上櫃股票資料，變成表格############################################################

#df = pd.read_csv(r[0].text, header = None)
print("                   ")
print("counter stock today colum name")
print(df_counter[0])
#print(df_buff.columns[1])
#print(df_buff.columns[2])
print("                   ")
print("                   ")
print("counter stock today are listed above")


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

mod_market_stock =[]
start_pos = 0
for stock in market_stock:
    for j in range(start_pos,len(df[0].index)):
        if(stock == df[0].iloc[j,0]):
            mod_market_stock.append(df[0].iloc[j,0])
            start_pos = j
            break

###########找出證券代號中對應的成交量並存於 deal_cnt_per_day#################
deal_cnt_per_day = []

#print("len of df")
#print(len(df[0].index))
#print("                 ")

#print("len of market_stock")
#print(len(market_stock))
#print("                 ")

import ast
start_pos = 0
for k in range(DaysToCalc):
    print("len of df")
    print(len(df[k].index))
    print("                 ")
    deal_cnt =[]
    stock_no =[]
    deal_price = []
    if(df[k]is None):
        print("dataframe on line not exist")
        print("-------------------")
        continue
    #########df的證券代號與 market_stock 比對後加入#########
    for i in range(int(len(mod_market_stock))):
        if(mod_market_stock[i] is None):
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
            if (mod_market_stock[i] == df[k].iloc[j,0]):
                stock_no.append(mod_market_stock[i])
                try:
                    d_p_tmp = ast.literal_eval(df[k].iloc[j,3])
                except:
                    d_p_tmp = -0.8787
                deal_price.append(d_p_tmp)
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
    df_data = {"STOCK_NO":stock_no, "DEAL_COUNT":deal_cnt, "DEAL_PRICE":deal_price}
    df_temp = pd.DataFrame(df_data)
    deal_cnt_per_day.append(df_temp)
    #
    #########df的證券代號與market_stock 比對後加入#########
    
print("deal count 1st day = ")    
print(deal_cnt_per_day[0].head(10))


''#################找出證券代號中對應的成交量並存於 deal_cnt_per_day#################

''' export deal cnt as json'''
for i in range(DaysToCalc):
    file_name_str = real_work_day[i].strftime("%Y%m%d")
    file_name_str = file_name_str+"DealCntStocks.json"
    deal_cnt_per_day[i].to_json(file_name_str, orient='records',force_ascii=False)

print("Deal Count To JSON is Done!!!")
''''export deal cnt as json '''


print("Caculating Days:")
print(len(deal_cnt_per_day))
import DealCnt

total_deal_cnt = DealCnt.CalDealCntSum(len(deal_cnt_per_day), deal_cnt_per_day)

file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str +="And"
file_name_str +=str(DaysToCalc)
file_name_str += "DaysBefore"
file_name_str = file_name_str+"DealCntSum.json"
deal_cnt_per_day[i].to_json(file_name_str, orient='records',force_ascii=False)
print("DealCntSum To JSON is Done!!!")


end_time = datetime.now()
print("-------------")
print("calculating time is")
print(end_time - start_time)

#print("Stock Cnt For Total Deal Count:")
#print(len(total_deal_cnt))


print("Total Deal Count From Function:")
print(total_deal_cnt)
#print(len(total_deal_cnt))

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

import GetOverDeal

OverDealDf = GetOverDeal(deal_cnt_per_day, total_deal_cnt)
'''    
deal_cnt_over_deal =[]
stock_no_over_deal =[]
deal_price_over_deal = []
total_deal_amount =[]

over_deal_num = 0
start_pos = 0
for stock_index in total_deal_cnt.index:
    deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["DEAL_COUNT"]])
    deal_cnt_today = int(deal_cnt_per_day[0].loc[stock_index,["DEAL_COUNT"]])
    deal_price_today = deal_cnt_per_day[0].loc[stock_index,["DEAL_PRICE"]]
    if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
        deal_cnt_over_deal.append(deal_cnt_today)
        stock_no_over_deal.append(deal_cnt_per_day[0].iloc[stock_index,0])
        deal_price_over_deal.append(deal_price_today)
        deal_amount_str = deal_price_today * deal_cnt_today
        
        
        total_deal_amount.append(deal_price_today * deal_cnt_today)
    
    print("deal_amount_str")
    try:
        print(deal_amount_str)
        print(type(deal_amount_str))
    except:
        print("total_deal_amount not exist")
    #deal_cnt_sum_no = total_deal_cnt.loc[stock_index,["證券代號"]]
    #deal_cnt_today_no = deal_cnt_per_day[0].loc[stock_index,["證券代號"]]
    #deal_cnt_today = 0
    #for i in range(start_pos,len(deal_cnt_per_day[0].index)):
        #deal_cnt_today_no_tmp = deal_cnt_per_day[0].loc[i,["證券代號"]]
        #print("證券代號")
        #print(deal_cnt_today_no_tmp)
        #if(deal_cnt_today_no_tmp == deal_cnt_sum_no):
        #    deal_cnt_today_no = deal_cnt_today_no_tmp
        #    deal_cnt_today = deal_cnt_per_day[0].loc[i,["成交股數"]]
        #    start_pos = i
        #    break
        
    
    #if(stock_index>len(deal_cnt_per_day[0])-1):
    #    print("total deal cnt num > deal_cnt_num_today")
    #    break;
    #deal_cnt_today = int(deal_cnt_per_day[0].loc[stock_index,["成交股數"]])
        
over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal, "DEAL_AMOUNT":total_deal_amount}
OverDealDf = pd.DataFrame(over_deal_data)

''######################################找今天交易量大於前幾天總和的股票######################################

'''
file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"OverDealStocks.json"
OverDealDf.to_json(file_name_str, orient='records')
#for day in range(DaysToCalc):
#print("-------------")
#print("deal cnt Day 0")
#print(deal_cnt_per_day[day].head(50))
#print("             ")
    

#str_buff = "deal cnt sum for " + str(DaysToCalc)
#str_buff = str_buff + " days:"
#print("-------------")
#print(str_buff)
#print(total_deal_cnt.head(50))
#print(total_deal_cnt.loc["成交股數"])#[1]deal_cnt_3day
#print("              ")
#print("              ")

file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"OverDealStocks.xlsx"
OverDealDf.to_excel(file_name_str)
print("-------------")
print("over deal stock")
print(OverDealDf)
print("-------------")
print("             ")

print("Computation is Done!!!!")
while(1):
    tm.sleep(1)
'''
total_deal_cnt_yesterday = DealCnt.CalDealCntSum( len(deal_cnt_per_day)-1, deal_cnt_per_day)
OverDealYesterday = DealCnt.FindOverDeal(total_deal_cnt_yesterday, deal_cnt_per_day[1])
print("-------------")
print("over deal yesterday")
print(OverDealYesterday)
print("-------------")
print("             ")

deal_cnt_df_today = deal_cnt_per_day[0]
over_deal_2_days = []
for stock_yesterday in OverDealYesterday:
    stock_today = deal_cnt_df_today.loc[deal_cnt_df_today['證券代號'] == stock_yesterday['STOCK_NO']]
    if(int(stock_today['成交股數']) > int(stock_yesterday['DEAL_COUNT'])):
        over_deal_2_days.append(stock_today)


print("-------------")
print("over deal 2days")
print(over_deal_2_days)
'''
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