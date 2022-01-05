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
        deal_cnt_total = total_deal_cnt.iloc[indx_in_dc_total,0]
        deal_price_today = deals_cnt_today.iloc[idex_in_dc_tday, 2]
        
        if(deal_cnt_today> (deal_cnt_total-deal_cnt_today)):
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deals_cnt_today.iloc[idex_in_dc_tday,0])
            deal_price_over_deal.append(deal_price_today)
            deal_amount_str = deal_price_today * deal_cnt_today
            total_deal_amount.append(deal_price_today * deal_cnt_today)
        '''
    for stock_index in total_deal_cnt.index:
        deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["DEAL_COUNT"]])
        stock_to_be_found = total_deal_cnt.loc[stock_index,["STOCK_NO"]]
        index_stock_today = -1
        for dc_today_index in range(start_pos ,len(deals_cnt_today.index)):
            stock_compare_to = deals_cnt_today.loc[dc_today_index,["STOCK_NO"]]
            if(str(stock_to_be_found) == str(stock_compare_to)):
                start_pos = dc_today_index
                index_stock_today = dc_today_index
                break
        
        if(index_stock_today < 0):
            error_str = "STOCK NO:"
            error_str = error_str+str(stock_to_be_found)
            error_str = error_str+"Not Found in Stocks today!!"
            print(error_str)
            break
        
        deal_cnt_today = int(deals_cnt_today.loc[index_stock_today,["DEAL_COUNT"]])
        deal_price_today_strs = str(deals_cnt_today.loc[index_stock_today,["DEAL_PRICE"]]).split()
        
        try:
            deal_price_today = float(deal_price_today_strs[1])           
        except:
            deal_price_today = 0
            stock_no = total_deal_cnt.loc[stock_index,["STOCK_NO"]]
            error_str ="Deal Price of Stock No: "
            error_str+=str(stock_no)
            error_str+=" is not exist!!!!!"
            print(error_str)
            for d_str in deal_price_today_strs:
                print(d_str)
            print("---------------------------------")
            
            
        if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deals_cnt_today.iloc[stock_index,0])
            deal_price_over_deal.append(deal_price_today)
            deal_amount_str = deal_price_today * deal_cnt_today
            total_deal_amount.append(deal_price_today * deal_cnt_today)
        '''    
    
        '''
        print("deal_amount_str")
        try:
            print(deal_amount_str)
            print(type(deal_amount_str))
        except:
            print("total_deal_amount not exist")
        '''
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
    return OverDealDf


''' for OverDeal test
import GetWorkedDay
import json
from datetime import datetime, timedelta, date

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2021, 11, 29))
real_work_day.append(date(2021, 11, 26))
real_work_day.append(date(2021, 11, 25))
real_work_day.append(date(2021, 11, 24))
real_work_day.append(date(2021, 11, 23))
real_work_day.append(date(2021, 11, 22))
real_work_day.append(date(2021, 11, 19))


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
    print(file_name_str)
    f = open(file_name_str)
    deal_cnt_stock = json.load(f)
    df_dcs = pd.DataFrame(deal_cnt_stock)
    prt_str = "DEAL COUNT OF DAY " + str(i)
    print(prt_str)
    print(df_dcs)
    for stock_data in deal_cnt_stock:
        stock_no_per_day.append(stock_data["STOCK_NO"])
        cnt_per_day.append(stock_data["DEAL_COUNT"])
        price_per_day.append(stock_data["DEAL_PRICE"])
    
    
    deal_cnt_data = {"STOCK_NO":stock_no_per_day, "DEAL_COUNT":cnt_per_day, "DEAL_PRICE":price_per_day}
    df = pd.DataFrame(deal_cnt_data)
    stock_no_per_day.clear()
    cnt_per_day.clear()
    price_per_day.clear()
    #print("DEAL CNT OF DAY")
    #print(i)
    #print("---------------------")
    #print(df)
    deal_cnt_per_day.append(df)
'''    
    
'''

#f = open("20211126And7DaysDealCntSum.json")
#,orient='values',encoding='utf-8'
total_deal_cnt = pd.read_json("20211129And7DaysBeforeDealCntSum.json")
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
for DealCntSum test'''