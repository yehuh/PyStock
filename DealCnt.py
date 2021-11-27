# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:35:17 2021

@author: yehuh
"""

import pandas as pd
import copy

def CalDealCntSum(calc_days, deal_cnt_per_day):
    if(calc_days>len(deal_cnt_per_day)):
        print("CalDealCntSum Failed!!!")
        return 1
    print("CalDealCntSum Started!!!")
    deal_cnt_per_day_rev = []
    total_df = len(deal_cnt_per_day)
    for i in range(total_df):
        deal_cnt_per_day_rev.append(deal_cnt_per_day[i])
        
    DealCntSum = copy.copy(deal_cnt_per_day_rev[0])
    #print("Deal Count of Today")
    #print(deal_cnt_per_day_rev)
    #print("                   ")
    #print("-------------------")
    
    start_pos = 0
    for day in range(1,calc_days):
        for stock_index in deal_cnt_per_day_rev[day].index:
            stock_to_found = deal_cnt_per_day_rev[day].loc[stock_index,["STOCK_NO"]]
            for tdc_index in range(start_pos ,len(DealCntSum.index)):
                stock_compare_to = DealCntSum.loc[tdc_index,["STOCK_NO"]]
                if(str(stock_to_found) == str(stock_compare_to)):
                    buff = DealCntSum.loc[tdc_index,["DEAL_COUNT"]] + deal_cnt_per_day_rev[day].loc[stock_index,["DEAL_COUNT"]]
                    DealCntSum.loc[tdc_index,["DEAL_COUNT"]] = buff
                    start_pos = tdc_index
                    break
        
        prt_str ="Calculate of Day" + str(day)
        prt_str+=" is Done!!!"
        print(prt_str)
        start_pos = 0
    
    return DealCntSum


def FindOverDeal(total_deal_cnt, deal_cnt_today_df):
    deal_cnt_over_deal =[]
    stock_no_over_deal =[]

    for stock_index in total_deal_cnt.index:
        deal_cnt_sum = int(total_deal_cnt.loc[stock_index,["DEAL_COUNT"]])
        deal_cnt_today = int(deal_cnt_today_df.loc[stock_index,["成交股數"]])
        if(deal_cnt_today > (deal_cnt_sum- deal_cnt_today)):
            deal_cnt_over_deal.append(deal_cnt_today)
            stock_no_over_deal.append(deal_cnt_today_df.iloc[stock_index,0])
        
    over_deal_data = {"STOCK_NO":stock_no_over_deal, "DEAL_COUNT":deal_cnt_over_deal}
    OverDealDf = pd.DataFrame(over_deal_data)
    return OverDealDf

''' for DealCntSum test
import GetWorkedDay
import json
from datetime import datetime, timedelta, date

real_work_day = []#GetWorkedDay.GetWorkedDay(80)
real_work_day.append(date(2021, 11, 25))
real_work_day.append(date(2021, 11, 24))
real_work_day.append(date(2021, 11, 23))
real_work_day.append(date(2021, 11, 22))
real_work_day.append(date(2021, 11, 21))
real_work_day.append(date(2021, 11, 20))
real_work_day.append(date(2021, 11, 19))

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
        stock_no_per_day.append(stock_data["證券代號"])
        cnt_per_day.append(stock_data["成交股數"])
        price_per_day.append(stock_data["收盤價"])
    
    
    deal_cnt_data = {"證券代號":stock_no_per_day, "成交股數":cnt_per_day, "收盤價":price_per_day}
    df = pd.DataFrame(deal_cnt_data)
    stock_no_per_day.clear()
    cnt_per_day.clear()
    price_per_day.clear()
    print("DEAL CNT OF DAY")
    print(i)
    print("---------------------")
    print(df)
    deal_cnt_per_day.append(df)

deal_cnt_sum =  CalDealCntSum(7, deal_cnt_per_day)

print("DEAL CNT SUM")
print(deal_cnt_sum)
for DealCntSum test'''