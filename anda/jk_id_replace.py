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


# ex = pd.read_excel('/Users/louisliu/Downloads/1.xlsx', sheet_name=0)
# ex1 = pd.read_excel('/Users/louisliu/Downloads/2.xlsx', sheet_name=0)

# ids = ex.merge(ex1, how='left', left_on='设备名称', right_on='设备名称')

# e = ex.copy()

# e.loc[e['设备来源']=='智能门锁系统', '业务主键'] = ids['business_key']

# e.to_excel('/Users/louisliu/Downloads/3.xlsx', index=False)


ex = pd.read_excel('/Users/louisliu/Downloads/1.xlsx', sheet_name=0)
ex1 = pd.read_excel('/Users/louisliu/Downloads/2.xlsx', sheet_name=0, skiprows=1)

ids = ex.merge(ex1, how='left', left_on='设备名称', right_on='设备名称')

e = ex.copy()

e['设备编号'] = ids['编号']
e['原始id'] = e['原始id'].astype(str)

e.to_excel('/Users/louisliu/Downloads/3.xlsx', index=False)