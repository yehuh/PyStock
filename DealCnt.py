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