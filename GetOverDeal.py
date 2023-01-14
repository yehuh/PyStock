# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 19:38:50 2021

@author: yehuh
"""
import pandas as pd
import copy


def getStockNoDF_V2(stock_df_big, stock_df_small, dispLog = False):#first_stock_df,sec_stock_df):
    start_pos = 0
    big_index = []
    big_df_stock_no = []
    small_df_stock_no = []
    small_index = []
    #first_stock_num = len(first_stock_df)
    #sec_stock_num =len(sec_stock_df)
    #if(first_stock_num > sec_stock_num):
    #    stock_df_big = first_stock_df
    #    stock_df_small = sec_stock_df
    #else:
    #    stock_df_big = sec_stock_df
    #    stock_df_small = first_stock_df

    big_df_buff = copy.copy(stock_df_big)
    big_df_buff.sort_values("STOCK_NO", inplace = True)
    #print(big_df_buff)
    small_df_buff = copy.copy(stock_df_small)
    small_df_buff.sort_values("STOCK_NO", inplace = True)
    #print(small_df_buff)
    for stock_large_index in range(len(big_df_buff)):#range(total_stocks):#
        stock_to_be_found = big_df_buff.iat[stock_large_index,0]
        index_in_stock_df_small_as_large_df =-1
        for stock_small_index in range(start_pos,len(small_df_buff)):
            stock_compare_to = small_df_buff.iat[stock_small_index,0]
            if(str(stock_to_be_found) == str(stock_compare_to)):
                start_pos = stock_small_index
                index_in_stock_df_small_as_large_df = stock_small_index
                break
            if(int(stock_compare_to) > int(stock_to_be_found)):
                error_str = "STOCK_NO:"
                error_str = error_str + str(stock_to_be_found)
                error_str = error_str+" IS NOT EXIST IN SMALL STOCK DF!!!"
                if(dispLog == True):
                    print(error_str)
                break
        
        if(index_in_stock_df_small_as_large_df<0):
            continue

        
        
        big_index.append(int(stock_large_index))
        big_df_stock_no.append(big_df_buff.iat[stock_large_index,0])
        small_index.append(int(index_in_stock_df_small_as_large_df))
        small_df_stock_no.append(small_df_buff.iat[index_in_stock_df_small_as_large_df,0])
    
    index_data = {"BIG_INDEX":big_index, "SMALL_INDEX":small_index}
    StockNoIndexDF = pd.DataFrame(index_data)
    return StockNoIndexDF


def getStockNoDF(stock_df_big, stock_df_small, dispLog):
    start_pos = 0
    big_index = []
    small_index = []
    '''
    if(small_stocks > big_stocks):
        print("Small Stock Len:")
        print(str(small_stocks))
        print("Big Stock Len:")
        print(str(big_stocks))
        return -1
    ''' 
    for stock_large_index in stock_df_big.index:#range(total_stocks):#
        stock_to_be_found = stock_df_big.loc[stock_large_index,'STOCK_NO']
        index_in_stock_df_small_as_large_df =-1
        for stock_small_index in range(start_pos,len(stock_df_small.index)):
            stock_compare_to_str = str(stock_df_small.iloc[[stock_small_index],[0]]).split()
            stock_compare_to = stock_compare_to_str[2]
            if(str(stock_to_be_found) == str(stock_compare_to)):
                start_pos = stock_small_index
                index_in_stock_df_small_as_large_df = stock_small_index
                break
        
        if(index_in_stock_df_small_as_large_df<0):
            error_str = "STOCK_NO:"
            error_str = error_str + str(stock_to_be_found)
            error_str = error_str+" IS NOT EXIST IN SMALL STOCK DF!!!"
            if(dispLog == True):
                print(error_str)
            continue
        
        big_index.append(int(stock_large_index))
        small_index.append(int(index_in_stock_df_small_as_large_df))
    
    index_data = {"BIG_INDEX":big_index, "SMALL_INDEX":small_index}
    StockNoIndexDF = pd.DataFrame(index_data)
    return StockNoIndexDF


def GetOverDeal(deals_cnt_today, total_deal_cnt, dispLog = False):
    deal_cnt_over_deal =[]
    stock_no_over_deal =[]
    deal_price_over_deal = []
    total_deal_amount =[]
    
    dfStockNoDf = getStockNoDF_V2(total_deal_cnt, deals_cnt_today)
    if(dispLog == True):
        print(dfStockNoDf)
    #dfStockNoDf = getStockNoDF(total_deal_cnt, deals_cnt_today,False)
    for idex in dfStockNoDf.index:
        idex_in_dc_tday = dfStockNoDf.at[idex,'SMALL_INDEX']
        try:
            deal_cnt_today = int(deals_cnt_today.iat[idex_in_dc_tday, 1])
            indx_in_dc_total = dfStockNoDf.at[idex,'BIG_INDEX']
            deal_cnt_total = int(total_deal_cnt.iat[indx_in_dc_total,1])
            deal_price_today = float(deals_cnt_today.iat[idex_in_dc_tday, 2])
            stock_no = str(deals_cnt_today.iat[idex_in_dc_tday,0])
        except:
            print("Data of Stock " + stock_no+ " Is Not Exist!!")
            continue  #skip this index
        
        
        if(deal_cnt_today> (deal_cnt_total-deal_cnt_today)):
            if(dispLog == True):
                print("Data of Stock " + stock_no+ " Is OverDeal!!")
                print("Deal Today:  " + str(deal_cnt_today))
                print("Deal Totol: "+str(deal_cnt_total-deal_cnt_today))
                
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deals_cnt_today.iat[idex_in_dc_tday,0])
            deal_price_over_deal.append(deal_price_today)
            deal_amount_str = deal_price_today * deal_cnt_today
            total_deal_amount.append(deal_price_today * deal_cnt_today)

        
    over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal, "DEAL_AMOUNT":total_deal_amount}
    OverDealDf = pd.DataFrame(over_deal_data)
    return OverDealDf


''' for OverDeal test
import GetWorkedDay
import json
from datetime import datetime, timedelta, date
import DealCnt

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2022, 3, 31))
real_work_day.append(date(2022, 3, 30))
real_work_day.append(date(2022, 3, 29))
real_work_day.append(date(2022, 3, 28))
real_work_day.append(date(2022, 3, 25))
real_work_day.append(date(2022, 3, 24))
real_work_day.append(date(2022, 3, 23))
real_work_day.append(date(2022, 3, 22))
real_work_day.append(date(2022, 3, 21))



deal_cnt_per_day =[]
stock_no_per_day =[]
cnt_per_day =[]
price_per_day = []

file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"DealCntStocks.json"
f = open(file_name_str)
deal_cnt_stock = json.load(f)
#df_deal_cnt_today = pd.DataFrame(deal_cnt_stock)
df_deal_cnt_today = pd.read_json("20220415DealCntStocks.json")



#for i in range(7):
#    file_name_str = real_work_day[i].strftime("%Y%m%d")
#    file_name_str = file_name_str+"DealCntStocks.json"
#    #print(file_name_str)
#    f = open(file_name_str)
#    deal_cnt_stock = json.load(f)
#    df_dcs = pd.DataFrame(deal_cnt_stock)
    #prt_str = "DEAL COUNT OF DAY " + str(i)
    #print(prt_str)
    #print(df_dcs)
#    for stock_data in deal_cnt_stock:
#        stock_no_per_day.append(stock_data["STOCK_NO"])
#        cnt_per_day.append(stock_data["DEAL_COUNT"])
#        price_per_day.append(stock_data["DEAL_PRICE"])
    
    
#    deal_cnt_data = {"STOCK_NO":stock_no_per_day, "DEAL_COUNT":cnt_per_day, "DEAL_PRICE":price_per_day}
#    df = pd.DataFrame(deal_cnt_data)
#    stock_no_per_day.clear()
#    cnt_per_day.clear()
#    price_per_day.clear()
#    deal_cnt_per_day.append(df)
    
    


##total_deal_cnt = pd.read_json("2022_0121__0113_DealCntSum.json")
total_deal_cnt = pd.read_json("20220415And7DaysBeforeDealCntSum.json")
total_deal_cnt.sort_values("STOCK_NO", inplace = True)
total_deal_cnt.reset_index(drop=True, inplace=True)
df_deal_cnt_today.sort_values("STOCK_NO", inplace = True)
df_deal_cnt_today.reset_index(drop=True, inplace=True)

print("Total Deal Count IS:")
print(total_deal_cnt)
print("Deal Cnt of Today is:")
print(df_deal_cnt_today)


over_deal_stock = GetOverDeal(df_deal_cnt_today, total_deal_cnt)
print("OVER DEAL STOCKS")
print(over_deal_stock)
index_df = getStockNoDF_V2(total_deal_cnt, over_deal_stock,False)
#index_df = getStockNoDF(total_deal_cnt, over_deal_stock, False)
#print(df_deal_cnt_today.iloc[index_df.SMALL_INDEX])
print("OVER DEAL TOTAL CNT STOCK")

#big_df_buff = copy.copy(total_deal_cnt)
#big_df_buff.sort_values("STOCK_NO", inplace = True)
over_df = total_deal_cnt.iloc[index_df.BIG_INDEX]
print(over_df)

#print(index_df)


#for idex in range(len(index_df.index)):
#    id_for_total_cnt = index_df.iat[idex,0]
#    if(id_for_total_cnt == first_id):
#        continue
#    over_df.append(total_deal_cnt.iat[id_for_total_cnt,])
#print("INDEX DATAFRAME:")
#print(df_test)
for DealCntSum test'''


'''for getStockNoDF_V2 test

import GetWorkedDay
import json
from datetime import datetime, timedelta, date
#import DealCnt

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2022, 3, 31))
real_work_day.append(date(2022, 3, 30))
real_work_day.append(date(2022, 3, 29))
real_work_day.append(date(2022, 3, 28))
real_work_day.append(date(2022, 3, 25))
real_work_day.append(date(2022, 3, 24))
real_work_day.append(date(2022, 3, 23))
real_work_day.append(date(2022, 3, 22))
real_work_day.append(date(2022, 3, 21))

file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"DealCntStocks.json"
f = open(file_name_str)
deal_cnt_stock = json.load(f)
big_df = pd.DataFrame(deal_cnt_stock)
big_df.sort_values("STOCK_NO", inplace=True)
print("BIG DF")
print(big_df.tail(20))
print("-------------------")
big_df.reset_index(drop=True, inplace=True)
print("BIG DF Reindex")
print(big_df.tail(20))
print("-------------------")
file_name_str = real_work_day[4].strftime("%Y%m%d")
file_name_str = file_name_str+"DealCntStocks.json"
f = open(file_name_str)
deal_cnt_stock = json.load(f)
small_df = pd.DataFrame(deal_cnt_stock)
small_df.sort_values("STOCK_NO", inplace=True)
print("SMALL DF")
print(small_df.tail(20))
print("-------------------")
small_df.reset_index(drop=True, inplace=True)
print("SMALL DF Reindex")
print(small_df.tail(20))
print("-------------------")

stock_no_df = getStockNoDF_V2(big_df, small_df,True)

print("Stock No Df")
print(stock_no_df)

for getStockNoDF_V2 test'''