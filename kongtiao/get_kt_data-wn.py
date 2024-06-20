import pandas as pd
import numpy as np
import json

def genKey(value):
    if (int(float(value)) == float(value)):
        return int(float(value))
    return value

map = {}
columns = ['通讯地址', '地址','名称', '点位']

for i in range(3):
    df_f = pd.read_excel(f'/home/coder/project/pandas/kongtiao/{i+1}f.xlsx', sheet_name=0, usecols=lambda c: c in columns, skiprows=2)
    df_f.rename(columns={'端口': 'n1', '通讯地址': 'n', '地址': 'address', '名称': 'name', '点位': 'deviceId'}, inplace=True)

    df_f.ffill(inplace=True)

    df_f['n'] = df_f['n'].astype(str)
    df_f['n'] = df_f['n'].apply(lambda value: genKey(value))

    grouped = df_f.groupby(['n'])

    for index, g in grouped:
        # 楼层map
        main_key = f"{i+1}F-{g.iloc[0].iloc[0]}"
        sub_map = {}
        for idx, row in g.iterrows():
            # 空调点位map
            sub_key = row.loc['address']
            sub_map[sub_key] = row[1:].to_dict()
        map[main_key] = sub_map

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('/home/coder/project/pandas/kongtiao/kongtiao.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

