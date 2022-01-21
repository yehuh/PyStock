# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 19:38:50 2021

@author: yehuh
"""
import pandas as pd

def getStockNoDF(stock_df_big, stock_df_small):
    start_pos = 0
    big_index = []
    small_index = []
    big_stocks = len(stock_df_big.index)
    small_stocks =len(stock_df_small.index)
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
            print(error_str)
        
        big_index.append(int(stock_large_index))
        small_index.append(int(index_in_stock_df_small_as_large_df))
    
    index_data = {"BIG_INDEX":big_index, "SMALL_INDEX":small_index}
    StockNoIndexDF = pd.DataFrame(index_data)
    return StockNoIndexDF


def GetOverDeal(deals_cnt_today, total_deal_cnt):
    deal_cnt_over_deal =[]
    stock_no_over_deal =[]
    deal_price_over_deal = []
    total_deal_amount =[]
    
    dfStockNoDf = getStockNoDF(total_deal_cnt, deals_cnt_today)
    over_deal_num = 0
    start_pos = 0
    test_cnt =0
    for idex in dfStockNoDf.index:
        idex_in_dc_tday = dfStockNoDf.loc[idex,'SMALL_INDEX']
        deal_cnt_today = deals_cnt_today.iloc[idex_in_dc_tday, 1]
        indx_in_dc_total = dfStockNoDf.loc[idex,'BIG_INDEX']
        deal_cnt_total = total_deal_cnt.iloc[indx_in_dc_total,1]
        deal_price_today = deals_cnt_today.iloc[idex_in_dc_tday, 2]
        
        if(deal_cnt_today> (deal_cnt_total-deal_cnt_today)):
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deals_cnt_today.iloc[idex_in_dc_tday,0])
            deal_price_over_deal.append(deal_price_today)
            deal_amount_str = deal_price_today * deal_cnt_today
            total_deal_amount.append(deal_price_today * deal_cnt_today)

        
    over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal, "DEAL_AMOUNT":total_deal_amount}
    OverDealDf = pd.DataFrame(over_deal_data)
    return OverDealDf


''' for OverDeal test'''
import GetWorkedDay
import json
from datetime import datetime, timedelta, date
import DealCnt

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2022, 1, 21))
real_work_day.append(date(2022, 1, 20))
real_work_day.append(date(2022, 1, 19))
real_work_day.append(date(2022, 1, 18))
real_work_day.append(date(2022, 1, 17))
real_work_day.append(date(2022, 1, 14))
real_work_day.append(date(2022, 1, 13))
real_work_day.append(date(2022, 1, 12))
real_work_day.append(date(2022, 1, 11))


deal_cnt_per_day =[]
stock_no_per_day =[]
cnt_per_day =[]
price_per_day = []

file_name_str = real_work_day[0].strftime("%Y%m%d")
file_name_str = file_name_str+"DealCntStocks.json"
f = open(file_name_str)
deal_cnt_stock = json.load(f)
df_deal_cnt_today = pd.DataFrame(deal_cnt_stock)
'''

'''
for i in range(7):
    file_name_str = real_work_day[i].strftime("%Y%m%d")
    file_name_str = file_name_str+"DealCntStocks.json"
    #print(file_name_str)
    f = open(file_name_str)
    deal_cnt_stock = json.load(f)
    df_dcs = pd.DataFrame(deal_cnt_stock)
    #prt_str = "DEAL COUNT OF DAY " + str(i)
    #print(prt_str)
    #print(df_dcs)
    for stock_data in deal_cnt_stock:
        stock_no_per_day.append(stock_data["STOCK_NO"])
        cnt_per_day.append(stock_data["DEAL_COUNT"])
        price_per_day.append(stock_data["DEAL_PRICE"])
    
    
    deal_cnt_data = {"STOCK_NO":stock_no_per_day, "DEAL_COUNT":cnt_per_day, "DEAL_PRICE":price_per_day}
    df = pd.DataFrame(deal_cnt_data)
    stock_no_per_day.clear()
    cnt_per_day.clear()
    price_per_day.clear()
    deal_cnt_per_day.append(df)
'''    
    
'''

total_deal_cnt = pd.read_json("2022_0121__0113_DealCntSum.json")
print("Total Deal Count IS:")
print(total_deal_cnt)

print("Deal Cnt of Today is:")
print(df_deal_cnt_today)


#df_test = getStockNoDF(total_deal_cnt, df_deal_cnt_today)
#print("INDEX DATAFRAME:")
#print(df_test)
over_deal_stock = GetOverDeal(df_deal_cnt_today, total_deal_cnt)
print("OVER DEAL STOCKS")
print(over_deal_stock)
'''for DealCntSum test'''