
# - * - coding: utf - 8 -*-
#
# 作者：田豐(FontTian)
# 建立時間:'2017/7/16'
# 郵箱：fonttian@Gmaill.com
# CSDN：http://blog.csdn.net/fontthrone
import sys
import pandas as pd
import json
import re
from importlib import reload
reload(sys)
sys.setdefaultencoding('utf-8')
class DataFrameToJSONArray():
    def __init__(self, dataframe, filepath='DataFrameToJSONArrayFile.json'):
        self.__DataFrame = dataframe
        self.__FilePath = filepath
    def funChangeDataFrameType(self):
        for i in range(len(self.__DataFrame.columns)):
            s = re.sub(r'\'>', '', re.sub(r'\d', '', str(type(self.__DataFrame.iloc[:, i][0])))).replace('\'', ' ').replace('.',' ').split(' ')[-1]
            if s == 'Timestamp':
                self.__DataFrame.iloc[:, i] = self.__DataFrame.iloc[:, i].astype(str)
            else:
                self.__DataFrame.iloc[:, i] = self.__DataFrame.iloc[:, i].astype(s)
            return self.__DataFrame
    def funSaveJSONArrayFile(self):
        list001 = []
        for i in range(len(self.__DataFrame.columns)):
            list001.append(list(self.__DataFrame.iloc[:, i]))
            list002 = []
            list003 = []
            for i in range(len(list001[0])):
                for j in range(len(self.__DataFrame.columns)):
                    list003.append(list001[j][i])
                    list002.append(list003)
                    list003 = []
                    Final_JSON = json.dumps(list002, sort_keys=True, indent=4, ensure_ascii=False)
                    with open(self.__FilePath, 'w') as f:
                        f.write(Final_JSON)
        return Final_JSON