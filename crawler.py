from datetime import datetime, timedelta
#import urllib2, logging, csv, re
#import requests
from io import StringIO
import pandas as pd
import numpy as np

daterange = datetime.today()

# 下載股價
days_ago = [15]
worked_day = [10]

days_ago = np.array([datetime.today() - timedelta(days =i) for i in range(30)]) 

worked_day = np.array([datetime.today() - timedelta(days =i) for i in range(10)])

j= 0
for i in range(30):
    if(days_ago[i].weekday() <5):
        #print(days_ago[i])
        if(j<10):
            worked_day[j] = days_ago[i]
        
        j = j+1
        
for i in range(10):
    print(worked_day[i].date())

        
#for i in range(10):
 #   r[i] = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + worked_day[i] + '&type=ALL')
    # 整理資料，變成表格
  #  df = pd.read_csv(StringIO(r.text.replace("=", "")),header=["證券代號" in l for l in r[i].text.split("\n")].index(True)-1)
    # 整理一些字串：
   # df = df.apply(lambda s: pd.to_numeric(s.astype(str).str.replace(",", "").replace("+", "1").replace("-", "-1"), errors='coerce'))
    #df.head()



# 顯示出來
#