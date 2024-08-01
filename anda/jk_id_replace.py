import pandas as pd
import numpy as np
import os

ex = pd.read_excel('/Users/louisliu/Downloads/1.监控-all.xlsx', sheet_name=0)

ex1 = pd.read_excel('/Users/louisliu/Downloads/监控-新业务id.xlsx', sheet_name=0)

ids = ex.merge(ex1, how='left', left_on='原始id', right_on='原始id')
print(ids)

e = ex.copy()
e['业务主键'] = ids['业务主键_y']

e.to_excel('/Users/louisliu/Downloads/1.监控.xlsx', index=False)
