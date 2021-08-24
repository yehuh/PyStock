# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 22:13:45 2021

@author: yehuh
"""

import pandas as pd
import json


from enum import Enum
class eStockType(Enum):
    MARKET = 1
    CONTER = 2

MarketStockURL = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
CounterStockURL = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"

def GetStockNo(stock_type):
    stock_no =[]
    if not isinstance(stock_type, eStockType):
        raise TypeError('stock_type must be an instance of eStockType Enum')
        return stock_no
    
    stock_no_url = MarketStockURL
    if(stock_type.value == eStockType.CONTER.value):
        stock_no_url = CounterStockURL
        
    market_stock = pd.read_html(stock_no_url)
    df_market = market_stock[0]
    m_stock_names =df_market.loc[:,2]

    stock_no =[]
    for i in range(1, len(m_stock_names.index)):
	    stock_str = m_stock_names.iloc[i].split()
	    stock_no.append(stock_str[0])

    #with open('market_stock_no_wahaha.json', 'w') as m_stock_id:
	#    json.dump(stock_no, m_stock_id)
        
    return stock_no

