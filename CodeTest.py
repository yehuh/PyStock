# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:27:44 2021

@author: yehuh
"""
import pandas as pd
#import DataFrameToJSONArray
import json
import DealCnt

from datetime import datetime, timedelta, date, time


import GetWorkedDay

#deal_cnt_per_day[0].to_json(r'C:\Users\yehuh\py_stock\deal_count_today.json',force_ascii=False)
#deal_cnt_per_day[1].to_json(r'C:\Users\yehuh\py_stock\deal_count_yesterday.json',force_ascii=False)

print(datetime.now().time())

stock_closed_time = time(15, 0,0)
print (stock_closed_time)






deal_cnt_p_day = []

deal_cnt_p_day.append(pd.read_json(r'C:\Users\yehuh\py_stock\deal_count_today.json'))
deal_cnt_p_day.append(pd.read_json(r'C:\Users\yehuh\py_stock\deal_count_yesterday.json'))
deal_cnt_p_day.append(pd.read_json(r'C:\Users\yehuh\py_stock\deal_count_yesterday.json'))
deal_cnt_p_day.append(pd.read_json(r'C:\Users\yehuh\py_stock\deal_count_yesterday.json'))
deal_cnt_p_day.append(pd.read_json(r'C:\Users\yehuh\py_stock\deal_count_yesterday.json'))
deal_cnt = DealCnt.CalDealCntSum(5,deal_cnt_p_day)
OverDeal = DealCnt.FindOverDeal(deal_cnt, deal_cnt_p_day[0])


print('DEAL COUNT PER DAY')
print(deal_cnt_p_day[0].head(50))
print('-------------------')
print('-------------------')
print('-------------------')
print('-------------------')
print('                   ')
print(deal_cnt_p_day[1].head(50))
print('-------------------')
print('-------------------')
print('-------------------')
print('-------------------')
print('                   ')

print('SUM OF DEAL COUNT')
print(deal_cnt)
print('-------------------')
print('-------------------')
print('-------------------')
print('                   ')


print('Over Deal Stock')
print(OverDeal)

