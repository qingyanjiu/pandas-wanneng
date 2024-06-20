import pandas as pd
import numpy as np
import json

map = {}
ex = pd.read_excel('/home/coder/project/pandas/new.xlsx', sheet_name=0, usecols=lambda c: \
    c != '楼层' and c.find('ignore') == -1 and c != '名称' and c != '摄像机类型' and c != '用户名账号' and c != '密码'\
        , skiprows=1)

ex.fillna('', inplace=True)

for index, row in ex.iterrows():
    if row[0] != '':
        if row['stream'] != '':
            row['stream'] = str(round(float(row['stream'])))
        map[row[0]] = row.to_dict()

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('jk.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

