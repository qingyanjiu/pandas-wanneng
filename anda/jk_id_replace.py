import pandas as pd
import numpy as np
import os

# ex = pd.read_excel('/Users/louisliu/Downloads/1.监控-all.xlsx', sheet_name=0)
# ex1 = pd.read_excel('/Users/louisliu/Downloads/监控-新业务id.xlsx', sheet_name=0)

# ids = ex.merge(ex1, how='left', left_on='原始id', right_on='原始id')
# print(ids)

# e = ex.copy()
# e['业务主键'] = ids['业务主键_y']

# e.to_excel('/Users/louisliu/Downloads/1.监控.xlsx', index=False)


ex = pd.read_excel('~/Desktop/安大-区域点位导入/设备绑定表格/已绑定code/3.安防绑定+门锁.xlsx', sheet_name=0)
ex1 = pd.read_excel('/Users/louisliu/Downloads/afid.xlsx', sheet_name=0)

ids = ex.merge(ex1, how='left', left_on='原始id', right_on='device_guid')

e = ex.copy()

e.loc[e['设备来源']=='智能门锁系统', '业务主键'] = ids['business_key']

e.to_excel('/Users/louisliu/Downloads/3.安防绑定+门锁.xlsx', index=False)