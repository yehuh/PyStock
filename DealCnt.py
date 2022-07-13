# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:35:17 2021

@author: yehuh
"""

import pandas as pd
import copy
import GetOverDeal

def CalDealCntSumV2(deal_cnt_per_days, dispLog = False):
    
    daysTotal = len(deal_cnt_per_days)
    smallest_deal_cnt_day =0
    smallest_stock_amount = 2000
    for i in range(daysTotal):
        if(len(deal_cnt_per_days[i])<smallest_stock_amount):
            smallest_deal_cnt_day = i
            smallest_stock_amount = len(deal_cnt_per_days[i])
    
    if(dispLog == True):
        print("Smallest Stock Amount is:")
        print(str(smallest_stock_amount))
        print("Smallest Stock Amount in Day " + str(smallest_deal_cnt_day))
    
    #rank_by_stock_no_df = copy.copy(deal_cnt_per_days[smallest_deal_cnt_day])
    #rank_by_stock_no_df.sort_values("STOCK_NO", inplace = True)
    funcResult = copy.copy(deal_cnt_per_days[smallest_deal_cnt_day])
    funcResult.sort_values("STOCK_NO", inplace = True)
    
    #print("rank_by_stock_no_df")
    #print(rank_by_stock_no_df)
    for day in range(daysTotal):
        if(day == smallest_deal_cnt_day):
            continue
        
        deal_cnt_per_days[day].sort_values("STOCK_NO", inplace = True)
        deal_cnt_per_days[day].reset_index(drop=True, inplace=True)
        ordered_stock_df = GetOverDeal.getStockNoDF_V2(
            deal_cnt_per_days[day], funcResult, False)
        #if(day==0):
        #    print(ordered_stock_df)
        if(dispLog == True):
            print("Stock Order")
            print(ordered_stock_df)
        
#        debugFlag = False
#        print_num = 2
#        print_counter =0
        deal_cnt_df = deal_cnt_per_days[day]
        for i in range(len(ordered_stock_df)):
            small_df_id = ordered_stock_df.iat[i,1]
            big_df_id = ordered_stock_df.iat[i,0]
            try:
                buff = funcResult.iat[small_df_id,1] + deal_cnt_df.iat[big_df_id,1]
            except:
                stock_no = str(deal_cnt_df.iat[big_df_id,0])
                print("SUM Of STOCK NO: " + stock_no +" Is Failed!!")
                continue
                
            funcResult.iat[int(small_df_id),1] = buff
            
    
    return funcResult
            


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


''' for DealCntSum test
import GetWorkedDay
import json
from datetime import datetime, timedelta, date

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
#real_work_day.append(date(2022, 4, 15))
#real_work_day.append(date(2022, 4, 14))
#real_work_day.append(date(2022, 4, 13))
#real_work_day.append(date(2022, 4, 12))
#real_work_day.append(date(2022, 4, 11))
#real_work_day.append(date(2022, 4, 8))
#real_work_day.append(date(2022, 4, 7))
#real_work_day.append(date(2022, 4, 6))



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
    df.sort_values("STOCK_NO", inplace = True)
    df.reset_index(drop=True, inplace=True)
    
    stock_no_per_day.clear()
    cnt_per_day.clear()
    price_per_day.clear()
    print("DEAL CNT OF DAY")
    print(i)
    print("---------------------")
    print(df)
    print("---------------------")
    print("DEAL CNT AFTER INDEX")
    #df.set_index("STOCK_NO", inplace = True)
    #print(df)
    deal_cnt_per_day.append(df)



#deal_cnt_sum =  CalDealCntSum(7, deal_cnt_per_day)


#print("DEAL CNT SUM")
#print(deal_cnt_sum)
#file_name_str = "2022_0121__0113_DealCntSum.json"
#deal_cnt_sum.to_json(file_name_str, orient='records',force_ascii=False)


deal_sum = CalDealCntSumV2(deal_cnt_per_day, False)
print("DEAL CNT SUM V2")
print(deal_sum)


for DealCntSum test'''