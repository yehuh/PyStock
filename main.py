# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:08:07 2022

@author: yehuh
"""
import GetWorkedDay
#import GetStockDataOnline
from datetime import datetime, timedelta, date, time
#import DealCnt
#import GetOverDeal
#import ToGoogleCloud

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    #start_time = datetime.now()
    real_work_day = GetWorkedDay.GetWorkedDay(5)
    #count_days = 7
    #deal_cnt_per_day = GetStockDataOnline.GetStockData(count_days)
    '''
    total_deal_cnt = DealCnt.CalDealCntSumV2(deal_cnt_per_day,False)
    total_deal_cnt.sort_values("STOCK_NO", inplace = True)
    total_deal_cnt.reset_index(drop=True, inplace=True)
    
    OverDealDf = GetOverDeal.GetOverDeal(deal_cnt_per_day[0], total_deal_cnt)

    real_work_day = GetWorkedDay.GetWorkedDay(count_days)
    work_day =[]
    for idex in OverDealDf.index:
        work_day.append(real_work_day[0].date())
        try:
            deal_amount =  float(OverDealDf.at[idex, "DEAL_AMOUNT"])
        except:
            stock_no = str(OverDealDf.at[idex,"STOCK_NO"])
            OverDealDf.drop([idex], axis = 0, inplace = True)
            continue



    OverDealDf["DATE"] = work_day
    OverDealDf_k_milium = OverDealDf[OverDealDf.DEAL_AMOUNT > 1000000000]
    
    df_from_cloud = ToGoogleCloud.GetDF_FromGCP()

    work_day_exist = False

    for idex in OverDealDf.index:
        if(real_work_day[0].date() ==  OverDealDf.at[idex, "DATE"]):
            work_day_exist = True
            print("Work day exist")
            break

    if(work_day_exist == False):
        ToGoogleCloud.DfToGoogleCloud(OverDealDf)
    
    '''
       
       
    
        
    #end_time = datetime.now()
    #print("calculating time is")
    #print(end_time - start_time)
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return str(real_work_day[0])


'''module test
start_time = datetime.now()

count_days = 7
deal_cnt_per_day = GetStockDataOnline.GetStockData(count_days)
print("Caculating Days:")
print(len(deal_cnt_per_day))


total_deal_cnt = DealCnt.CalDealCntSumV2(deal_cnt_per_day,False)
total_deal_cnt.sort_values("STOCK_NO", inplace = True)
total_deal_cnt.reset_index(drop=True, inplace=True)



OverDealDf = GetOverDeal.GetOverDeal(deal_cnt_per_day[0], total_deal_cnt)

real_work_day = GetWorkedDay.GetWorkedDay(count_days)
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

print("-------------")
print("over deal stock")
print(OverDealDf)
print("-------------")
print("             ")
print("DEAL_AMOUNT > 100000000")
print(OverDealDf[OverDealDf.DEAL_AMOUNT > 1000000000])
print("-------------")
print("             ")

print("Computation is Done!!!!")
end_time = datetime.now()
print("-------------")
print("calculating time is")
print(end_time - start_time)
module test'''