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


holidays_taiwan_2021.append(date(2022, 1, 1))
holidays_taiwan_2021.append(date(2022, 1, 27))
holidays_taiwan_2021.append(date(2022, 1, 28))
holidays_taiwan_2021.append(date(2022, 1, 31))
holidays_taiwan_2021.append(date(2022, 2, 1))
holidays_taiwan_2021.append(date(2022, 2, 2))
holidays_taiwan_2021.append(date(2022, 2, 3))
holidays_taiwan_2021.append(date(2022, 2, 4))
holidays_taiwan_2021.append(date(2022, 2, 28))
holidays_taiwan_2021.append(date(2022, 4, 4))
holidays_taiwan_2021.append(date(2022, 4, 5))
holidays_taiwan_2021.append(date(2022, 5, 2))
holidays_taiwan_2021.append(date(2022, 6, 3))
holidays_taiwan_2021.append(date(2022, 9, 9))
holidays_taiwan_2021.append(date(2022, 10, 10))

holidays_taiwan_2023 = []
holidays_taiwan_2023.append(date(2022, 9, 9))
holidays_taiwan_2023.append(date(2022, 10, 10))
holidays_taiwan_2023.append(date(2023, 1, 2))
holidays_taiwan_2023.append(date(2023, 1, 18))
holidays_taiwan_2023.append(date(2023, 1, 19))
holidays_taiwan_2023.append(date(2023, 1, 20))
holidays_taiwan_2023.append(date(2023, 1, 23))
holidays_taiwan_2023.append(date(2023, 1, 24))
holidays_taiwan_2023.append(date(2023, 1, 25))
holidays_taiwan_2023.append(date(2023, 1, 26))
holidays_taiwan_2023.append(date(2023, 1, 27))
holidays_taiwan_2023.append(date(2023, 2, 27))
holidays_taiwan_2023.append(date(2023, 2, 28))
holidays_taiwan_2023.append(date(2023, 4, 3))
holidays_taiwan_2023.append(date(2023, 4, 4))
holidays_taiwan_2023.append(date(2023, 4, 5))
holidays_taiwan_2023.append(date(2023, 5, 1))
holidays_taiwan_2023.append(date(2023, 6, 22))
holidays_taiwan_2023.append(date(2023, 6, 23))
holidays_taiwan_2023.append(date(2023, 9, 29))
holidays_taiwan_2023.append(date(2023, 10, 9))
holidays_taiwan_2023.append(date(2023, 10, 10))
#1/20~29

special_work_day = []
special_work_day.append(date(2022, 1,   22))
special_work_day.append(date(2022, 9,   11))
special_work_day.append(date(2023, 1,   7))
special_work_day.append(date(2023, 3,   25))
special_work_day.append(date(2023, 6,   17))
special_work_day.append(date(2023, 9,   23))

def GetWorkedDay(count_days_from_today):
    days_ago = []
    for i in range(count_days_from_today):
        days_ago.append(datetime.today() - timedelta(days = i))
        
    worked_day = []
    real_work_day =[]

    for day in days_ago:
        if day.weekday() < 5:
            worked_day.append(day)
        else:
            for s_work_day in special_work_day:
                if day == s_work_day:
                    worked_day.append(day)
        
    
    for dayy in worked_day:
        was_holiday = False
        for holiday in holidays_taiwan_2023:
            if dayy.date() == holiday:
                was_holiday = True
                break
            
        if was_holiday == False:
            real_work_day.append(dayy)
            
    return real_work_day