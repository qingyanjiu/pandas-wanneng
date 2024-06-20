import pandas as pd
import numpy as np
import json

map = {}
ex = pd.read_excel('/home/coder/project/pandas/mj.xlsx', sheet_name='门禁问题', usecols=lambda c: c != '升级情况' and c!= '问题' and c!= '楼层', skiprows=1)

ex.rename(columns={
    '名称': 'name', 
    '位置': 'position', 
    'ip地址': 'ip', 
    '掩码': 'mask', 
    '网关': 'gateway', 
    '用户名账号': 'username',
    '密码': 'password'
    }, inplace=True)

ex.ffill(inplace=True)
ex.fillna('', inplace=True)

for index, row in ex.iterrows():
    key = row.loc['name']
    map[key] = row.iloc[1:].to_dict()

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('mj.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

