import math
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





# ex = pd.read_excel('/Users/louisliu/Downloads/3000.xlsx', sheet_name=0, skiprows=1)
# ex1 = pd.read_excel('/Users/louisliu/Downloads/wl.xlsx', sheet_name=0)
# ex2 = pd.read_excel('/Users/louisliu/Downloads/hj.xlsx', sheet_name=0)

# ex1_ids = ex1.merge(ex, how='left', left_on='设备名称', right_on='设备名称')
# ex2_ids = ex2.merge(ex, how='left', left_on='设备名称', right_on='设备名称')

# e1 = ex1.copy()
# e2 = ex2.copy()

# e1['空间位置'] = ex1_ids['空间位置_y']
# e1['原始id'] = e1['原始id'].astype(str)
# e2['空间位置'] = ex2_ids['空间位置_y']
# e2['原始id'] = e2['原始id'].astype(str)

# e3 = e1._append(e2)

# e3.to_excel('/Users/louisliu/Downloads/e3.xlsx', index=False)


# ex = pd.read_excel('/Users/louisliu/Downloads/3.xlsx', sheet_name=0)
# offset = 0
# loop_n = math.ceil(len(ex) / 100)
# for i in range(loop_n):
#     e = ex[offset: offset + 100]
#     e.to_excel(f'/Users/louisliu/Downloads/t/{i}.xlsx', index=False)
#     offset += 100
    
ex = pd.read_excel('/Users/louisliu/Downloads/ids.xlsx', sheet_name=0)
ex['设备名称'] = ex['设备名称'] + '_'
ex['原始id'] = ex['原始id'].astype(str)
ex.to_excel('/Users/louisliu/Downloads/eee.xlsx', index=False)