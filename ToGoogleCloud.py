# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:03:44 2022

@author: yehuh
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import os
import db_dtypes

def DfToGoogleCloud(OverDealDf, dispLog = False):
    credentials_path = './stocks-bigquery-key.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    credentials = service_account.Credentials.from_service_account_file('stocks-bigquery-key.json')
	
    client = bigquery.Client(credentials=credentials)
 
    table_id = 'big-crow-300216.stock.OverDealCount'
 
    job = client.load_table_from_dataframe(OverDealDf, table_id)
    job.result()
 
    table = client.get_table(table_id)

    if(dispLog == True):
        print(f'已存入{table.num_rows}筆資料到{table_id}')
    

def GetDF_FromGCP(dispLog=False):
    credentials_path = './stocks-bigquery-key.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    credentials = service_account.Credentials.from_service_account_file('stocks-bigquery-key.json')

    client = bigquery.Client(credentials=credentials)

    table_id = 'big-crow-300216.stock.OverDealCount'

    ##job = client.load_table_from_dataframe(OverDealDf, table_id)
    ##job.result()

    table = client.get_table(table_id)
    query_job = client.query("""
                             SELECT *
                             FROM stock.OverDealCount
                             LIMIT 1000 """)

    results = query_job.to_dataframe()
    if (dispLog == True):
        #print(f'已存入{table.num_rows}筆資料到{table_id}')
        #print("Table schema: {}".format(table.schema))
        #print("Table description: {}".format(table.description))
        print(results)


'''module test'''

import pandas as pd

deal_cnt =[]
stock_no =[]
deal_amount = []

deal_cnt.append(10)
deal_cnt.append(20)
deal_cnt.append(30)

stock_no.append("1234")
stock_no.append("5678")
stock_no.append("9012")

deal_amount.append(100.87)
deal_amount.append(200.87)
deal_amount.append(300.87)

#df_data = {"STOCK_NO":stock_no, "DEAL_COUNT":deal_cnt, "DEAL_AMOUNT":deal_amount}
#df = pd.DataFrame(df_data)

#DfToGoogleCloud(df, True)

GetFromGCP(True)

'''module test'''