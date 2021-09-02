# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 22:09:35 2021

@author: yehuh
"""

from datetime import datetime, timedelta, date


#設定2021的假日
holidays_taiwan_2021 = []
holidays_taiwan_2021.append(date(2021, 1, 1))
holidays_taiwan_2021.append(date(2021, 2, 10))
holidays_taiwan_2021.append(date(2021, 2, 11))
holidays_taiwan_2021.append(date(2021, 2, 12))
holidays_taiwan_2021.append(date(2021, 2, 15))
holidays_taiwan_2021.append(date(2021, 2, 16))
holidays_taiwan_2021.append(date(2021, 3, 1))
holidays_taiwan_2021.append(date(2021, 4, 2))
holidays_taiwan_2021.append(date(2021, 4, 5))
holidays_taiwan_2021.append(date(2021, 4, 30))
holidays_taiwan_2021.append(date(2021, 6, 14))
holidays_taiwan_2021.append(date(2021, 9, 20))
holidays_taiwan_2021.append(date(2021, 9, 21))
holidays_taiwan_2021.append(date(2021, 10, 11))
holidays_taiwan_2021.append(date(2021, 12, 31))


def GetWorkedDay(count_days_from_today):
    days_ago = []
    for i in range(count_days_from_today):
        days_ago.append(datetime.today() - timedelta(days = i))
        
    worked_day = []
    real_work_day =[]

    for day in days_ago:
        if day.weekday() < 5:
            worked_day.append(day)
    
    for dayy in worked_day:
        was_holiday = False
        for holiday in holidays_taiwan_2021:
            if dayy.date() == holiday:
                was_holiday = True
                break
            
        if was_holiday == False:
            real_work_day.append(dayy)
            
    return real_work_day