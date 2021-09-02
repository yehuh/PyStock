# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:35:17 2021

@author: yehuh
"""

import pandas
import copy

def CalDealCntSum(calc_days, deal_cnt_per_day):
    print(len(deal_cnt_per_day))
    deal_cnt_per_day_rev = []
    for i in range(len(deal_cnt_per_day)):
        total_df = len(deal_cnt_per_day)
        deal_cnt_per_day_rev.append(deal_cnt_per_day[total_df-i-1])
        
    DealCntSum = copy.copy(deal_cnt_per_day_rev[0])
    start_pos = 0
    for day in range(1,calc_days):
        for stock_index in deal_cnt_per_day_rev[day].index:
            stock_to_found = deal_cnt_per_day_rev[day].loc[stock_index,["證券代號"]]
            for tdc_index in range(start_pos ,len(DealCntSum.index)):
                stock_compare_to = DealCntSum.loc[tdc_index,["證券代號"]]
                if(str(stock_to_found) == str(stock_compare_to)):
                    buff = DealCntSum.loc[tdc_index,["成交股數"]] + deal_cnt_per_day_rev[day].loc[stock_index,["成交股數"]]
                    DealCntSum.loc[tdc_index,["成交股數"]] = buff
                    start_pos = tdc_index
                    break
                
        start_pos = 0;
    
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
    OverDealDf = pandas.DataFrame(over_deal_data)
    return OverDealDf
