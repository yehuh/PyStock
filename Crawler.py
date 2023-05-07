import pandas as pd
#import urllib2, logging, csv, re
import requests
from io import StringIO
from datetime import datetime, timedelta, date, time

import time as tm
#import DataFrameToJSONArray
import json
import GetWorkedDay
#import StockOnline
import GetStockDataOnline


#找出台股上市上櫃代號
#stock_noooo = StockOnline.GetStockNo(StockOnline.eStockType.CONTER)

#import time

start_time = datetime.now()

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

#market_stock = []
#market_stock.append(real_work_day[0].max)




DaysToCalc = 7
deal_cnt_per_day = GetStockDataOnline.GetStockData(DaysToCalc, False)

''' 
############################# export deal cnt as json #############################
for i in range(DaysToCalc):#():
    file_name_str = real_work_day[i+WorkDayShift].strftime("%Y%m%d")
    file_name_str = file_name_str+"DealCntStocks.json"
    deal_cnt_per_day[i].sort_values("STOCK_NO", inplace = True)
    deal_cnt_per_day[i].reset_index(drop=True, inplace=True)
    deal_cnt_per_day[i].to_json(file_name_str, orient='records',force_ascii=False)
    

print("Deal Count To JSON is Done!!!")
############################# export deal cnt as json #############################
'''

print("Caculating Days:")
print(len(deal_cnt_per_day))
import DealCnt
import copy

total_deal_cnt = DealCnt.CalDealCntSumV2(deal_cnt_per_day,False)
total_deal_cnt.sort_values("STOCK_NO", inplace = True)
total_deal_cnt.reset_index(drop=True, inplace=True)
deal_cnt_today  = copy.copy(deal_cnt_per_day[0])
deal_cnt_today.sort_values("STOCK_NO", inplace = True)
deal_cnt_today.reset_index(drop=True, inplace=True)
#total_deal_cnt = DealCnt.CalDealCntSum(DaysToCalc,deal_cnt_per_day)
#CalDealCntSum(calc_days, deal_cnt_per_day)
#(len(deal_cnt_per_day), deal_cnt_per_day)

''' 
######################## export DealCntSum as json ########################
file_name_str = real_work_day[WorkDayShift].strftime("%Y%m%d")
file_name_str +="And"
file_name_str +=str(DaysToCalc)
file_name_str += "DaysBefore"
file_name_str = file_name_str+"DealCntSum.json"
total_deal_cnt.to_json(file_name_str, orient='records',force_ascii=False)
print("DealCntSum To JSON is Done!!!")
######################## export DealCntSum as json ########################
'''

#print("Stock Cnt For Total Deal Count:")
#print(len(total_deal_cnt))


#print("Total Deal Count From Function:")
#print(total_deal_cnt)
#print(len(total_deal_cnt))


#print("Stock today")
#print(deal_cnt_per_day[0])

import GetOverDeal

OverDealDf = GetOverDeal.GetOverDeal(deal_cnt_today, total_deal_cnt, False)


'''
######################## OverDealDf to excel ########################
file_name_str = real_work_day[WorkDayShift].strftime("%Y%m%d")
file_name_str = file_name_str+"OverDealStocks.json"
OverDealDf.to_json(file_name_str, orient='records')


file_name_str = real_work_day[WorkDayShift].strftime("%Y%m%d")
file_name_str = file_name_str+"OverDealStocks.xlsx"
OverDealDf.to_excel(file_name_str)
######################## OverDealDf to excel ########################
'''


work_day =[]
for idex in OverDealDf.index:
    work_day.append(real_work_day[0].date())
    try:
        deal_amount =  float(OverDealDf.at[idex, "DEAL_AMOUNT"])
    except:
        stock_no = str(OverDealDf.at[idex,"STOCK_NO"])
        print("Deal Mount of Stock " + stock_no)
        print("is not Work!!!!")
        OverDealDf.drop([idex], axis = 0, inplace = True)
        continue



OverDealDf["DATE"] = work_day
OverDealDf_k_milium = OverDealDf[OverDealDf.DEAL_AMOUNT > 450000000]

'''
##################### To Stock Data To Cloud Google #####################
import ToGoogleCloud
df_from_cloud = ToGoogleCloud.GetDF_FromGCP()

work_day_exist = False

for idex in OverDealDf.index:
    if(real_work_day[0].date() ==  OverDealDf.at[idex, "DATE"]):
       work_day_exist = True
       print("Work day exist")
       break

if(work_day_exist == False):
    ToGoogleCloud.DfToGoogleCloud(OverDealDf_k_milium)
    print("Stock Data To Cloud Google")

##################### To Stock Data To Cloud Google #####################
'''       
       

print("-------------")
print("over deal stock")
print(OverDealDf)
print("-------------")
print("             ")
print("DEAL_AMOUNT > 450000000")
print(OverDealDf_k_milium)
print("-------------")
print("             ")


#stock_df = GetOverDeal.getStockNoDF_V2(total_deal_cnt, OverDealDf, False)
#print("-------------")
#print("STOCK POS")
#print(stock_df)






print("Computation is Done!!!!")
end_time = datetime.now()
print("-------------")
print("calculating time is")
print(end_time - start_time)




while(1):
    tm.sleep(1)