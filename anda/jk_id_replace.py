import json
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



# 合并xlsx和json
# ex = pd.read_excel('/Users/louisliu/Downloads/1.xlsx', sheet_name=0)
# ex1 = pd.read_json('/Users/louisliu/Downloads/2.json')
# ex1 = ex1.T
# ex1['code'] = ex1.apply(lambda x: x.name, axis=1)
# ids = ex.merge(ex1, how='left', left_on='设备名称', right_on='name')
# e = ex.copy()
# e['设备编号'] = ids['code']

# e.to_excel('/Users/louisliu/Downloads/3333.xlsx', index=False)




# ex = pd.read_excel('/Users/louisliu/Downloads/111.xlsx', sheet_name=0)
# ex1 = pd.read_excel('/Users/louisliu/Downloads/222.xls', sheet_name=1)
# ids = ex.merge(ex1, how='left', left_on='name', right_on='现房间号')
# e = ex.copy()
# e['设备编号'] = ids.apply(lambda x: x['code'] if pd.notnull(x['code']) else x['设备编号'], axis=1)

# e.to_excel('/Users/louisliu/Downloads/3333.xlsx', index=False)

def genCode(name):
    part = 'A' if name.find('A') > -1 else 'B'
    prefix = ''
    if name.find('空调') > -1:
        prefix = 'wty-ele-k-' + ('a-' if part == 'A' else 'b-')
    else:
        prefix = 'd-r-' + ('A' if part == 'A' else 'B')
    code = prefix + name.split('-')[-1]
    return code

ex = pd.read_excel('anda/11-elec-data.xlsx', sheet_name=0)

ex['设备编号'] = ex.apply(lambda x: genCode(x['设备名称']), axis=1)

ex.to_excel('/Users/louisliu/Downloads/3333.xlsx', index=False)