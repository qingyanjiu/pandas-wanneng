import pandas as pd
import numpy as np
import json

map = {}
columns = ['楼层', '房间号', '回路号', '开关控制', '开关反馈', '备注']

df_f = pd.read_excel(f'/home/coder/project/pandas/zhaoming/zm.xlsx', sheet_name=0, usecols=lambda c: c in columns, skiprows=0)
df_f.rename(columns={'楼层': 'f', '房间号': 'roomNo', '回路号': 'id', '开关控制': 'w_device_id', '开关反馈': 'r_device_id', '备注': 'remark'}, inplace=True)

df_f['f'] = df_f['f'].ffill()
df_f['roomNo'] = df_f['roomNo'].ffill()
df_f['w_device_id'] = df_f['w_device_id'].fillna('')
df_f['r_device_id'] = df_f['r_device_id'].fillna('')
df_f['remark'] = df_f['remark'].fillna('')
df_f['id'] = df_f['id'].fillna(0)
df_f['id'] = df_f['id'].astype(int)

df_f['f'] = df_f['f'].astype(int)
df_f['id'] = df_f['id'].astype(str)
df_f['roomNo'] = df_f['roomNo'].astype(str)

grouped = df_f.groupby(['r_device_id'])

for idx, g in grouped:
    # 楼层map
    if (g.iloc[0].loc['r_device_id'] != '' and g.iloc[0].loc['w_device_id'] != ''):
        main_key = f"{g.iloc[0].loc['f']}F-{g.iloc[0].loc['r_device_id']}"
        map[main_key] = {}
        map[main_key]['id'] = g.iloc[0].loc['id']
        map[main_key]['w_device_id'] = g.iloc[0].loc['w_device_id']
        map[main_key]['r_device_id'] = g.iloc[0].loc['r_device_id']
        sub_list = []
        for idx, row in g.iterrows():
            sub_list.append(row.loc[['roomNo', 'remark']].to_dict())
        map[main_key]['devices'] = sub_list

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('/home/coder/project/pandas/zhaoming/zhaoming.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

