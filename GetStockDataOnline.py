# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:23:21 2022

@author: yehuh
"""

import GetWorkedDay
from datetime import datetime, timedelta, date, time
import requests
import pandas as pd
from io import StringIO
import json
import ast

def GetStockData(day_cnt):
    real_work_day = GetWorkedDay.GetWorkedDay(80)

    stock_closed_time = time(15,0,0)
    WorkDayShift = 0
    if(date.today() ==  real_work_day[0].date()):
        print("today is work day")
        if(datetime.now().time() < stock_closed_time):
            print("Stock Dealing data of Today is not prepared")
            WorkDayShift =1
    else:
        print("today is not work day")

    roc_year = int(real_work_day[0].year) - 1911
    print("Year of ROC Now:")
    print(str(roc_year))


    ##############################下載股價##############################
    DaysToCalc = day_cnt
    r_counter=[]
    r_market=[]
    for i in range(DaysToCalc):
        roc_year_conter = int(real_work_day[i].year) - 1911
        r_counter.append(requests.post('https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d=' + str(roc_year_conter) + '/' + real_work_day[i+WorkDayShift].strftime("%m/%d") + '&s=0,asc,0'))
        r_market.append(requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + real_work_day[i+WorkDayShift].strftime("%Y%m%d") + '&type=ALL'))
        '' ##############################下載股價##############################
    
    
    
    ########################################整理上市股票資料，變成表格########################################
    df_market =[]
    for i in range(DaysToCalc):
        df_buff = pd.read_csv(StringIO(r_market[i].text.replace("=", "")), header=["證券代號" in l for l in     r_market[i].text.split("\n")].index(True)-1)
  
        df_buff1 = df_buff.drop(columns=["證券名稱","成交筆數","成交金額","開盤價","最高價","最低價"])#,"收盤價"
        df_buff2 = df_buff1.drop(columns=["最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"])
        df_buff2 = df_buff2.drop(columns=["漲跌(+/-)","Unnamed: 16"])
        columns_titles = ["證券代號","漲跌價差","成交股數","收盤價"]
        df_buff2=df_buff2.reindex(columns=columns_titles)
        df_buff3 = df_buff2.rename(columns = {"證券代號": "代號", "漲跌價差": "漲跌"}, inplace = False)
        df_market.append(df_buff3)
    '' ########################################整理上市股票資料，變成表格########################################
    
    
    ########################整理上櫃股票資料，變成表格########################
    couter_stock_data =[]
    df_counter =[]
    disp_flag = 0
    for idd in range(DaysToCalc):
        data_str_buff = r_counter[idd].text.split("\n")
        index_line = 0
        for i in range(len(data_str_buff)):
            if(data_str_buff[i].find("代號")!=-1):
                index_line = i
                break
    
        for i in range(index_line):
            data_str_buff.pop(0)            
            stock_data_index = data_str_buff[0].split(",")    

        index_str = ""
        for l in stock_data_index:
            buffd = '\"' + l.strip()
            buffd = buffd+ '\"'
            buffd = buffd+ ','
            index_str += buffd
    
        index_str = index_str.rstrip(',')

        data_str_buff.pop(0)
        data_str_buff.insert(0,index_str)

        couter_stock_data.append("")
        for data_str in data_str_buff:
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
    '' ########################整理上櫃股票資料，變成表格########################
    
    ########將上市與上櫃股票整合為一個表格########
    df =[]
    for dayk in range(DaysToCalc):
        df.append(pd.concat([df_market[dayk], df_counter[dayk]], ignore_index=True))
    '' ########將上市與上櫃股票整合為一個表格########
    
    
    ###############讀取證券代號並比對今日有交易的股票代號###############
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
    '' ###############讀取證券代號並比對今日有交易的股票代號###############



    ###########找出證券代號中對應的成交量並存於 deal_cnt_per_day#################
    deal_cnt_per_day = []




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
                    deal_cnt.append(int(d_c_temp))
                    #df的證券代號與 market_stock 為一對一且順序皆為由小到大
                    #=>下個證券代號從現在的位置找起
                    start_pos = j 
                    break;
                    
        start_pos = 0
        df_data = {"STOCK_NO":stock_no, "DEAL_COUNT":deal_cnt, "DEAL_PRICE":deal_price}
        df_temp = pd.DataFrame(df_data)
        deal_cnt_per_day.append(df_temp)
    
        #########df的證券代號與market_stock 比對後加入#########


    ''#################找出證券代號中對應的成交量並存於 deal_cnt_per_day#################
    return deal_cnt_per_day
    