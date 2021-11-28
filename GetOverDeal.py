# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 19:38:50 2021

@author: yehuh
"""
import pandas as pd
def GetOverDeal(deal_cnt_per_day, total_deal_cnt):
    deal_cnt_over_deal =[]
    stock_no_over_deal =[]
    deal_price_over_deal = []
    total_deal_amount =[]

    print("Deal------Price")
    deal_pr = str(deal_cnt_per_day[0].loc[0,["DEAL_PRICE"]])
    deal_str = deal_pr.split()
    print(float(deal_str[1]))
    

    
    
    
    error_str = "Stock no:"
    print(int(total_deal_cnt.loc[0,["DEAL_COUNT"]]))
    over_deal_num = 0
    start_pos = 0
    for stock_index in total_deal_cnt.index:
        deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["DEAL_COUNT"]])
        deal_cnt_today = int(deal_cnt_per_day[0].loc[stock_index,["DEAL_COUNT"]])
        deal_price_today_strs = str(deal_cnt_per_day[0].loc[stock_index,["DEAL_PRICE"]]).split()
        
        try:
            deal_price_today = float(deal_price_today_strs[1])
        except:
            deal_price_today = 0
            stock_no = total_deal_cnt.loc[stock_index,["STOCK_NO"]]
            error_str ="Deal Price of Stock No: "
            error_str+=str(stock_no)
            error_str+=" is not exist!!!!!"
            print(error_str)
            
        if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deal_cnt_per_day[0].iloc[stock_index,0])
            deal_price_over_deal.append(deal_price_today)
            deal_amount_str = deal_price_today * deal_cnt_today
            total_deal_amount.append(deal_price_today * deal_cnt_today)
    
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


''' for OverDeal test'''
import GetWorkedDay
import json
from datetime import datetime, timedelta, date

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2021, 11, 26))
real_work_day.append(date(2021, 11, 25))
real_work_day.append(date(2021, 11, 24))
real_work_day.append(date(2021, 11, 23))
real_work_day.append(date(2021, 11, 22))
real_work_day.append(date(2021, 11, 19))
real_work_day.append(date(2021, 11, 18))

deal_cnt_per_day =[]
stock_no_per_day =[]
cnt_per_day =[]
price_per_day = []
for i in range(7):
    file_name_str = real_work_day[i].strftime("%Y%m%d")
    file_name_str = file_name_str+"DealCntStocks.json"
    print(file_name_str)
    f = open(file_name_str)
    deal_cnt_stock = json.load(f)
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

#f = open("20211126And7DaysDealCntSum.json")
#,orient='values',encoding='utf-8'
total_deal_cnt = pd.read_json("20211126And7DaysBeforeDealCntSum.json")
print("Total Deal Count IS:")
print(total_deal_cnt)

over_deal_stock = GetOverDeal(deal_cnt_per_day, total_deal_cnt)
print("OVER DEAL STOCKS")
print(over_deal_stock)
''''for DealCntSum test'''