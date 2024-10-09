import sys
import pandas as pd
from pypinyin import lazy_pinyin

name_map = {
    '全景监控摄像机1': 'QJ1',
    '全景监控摄像机2': 'QJ2',
    '指挥球型摄像机': 'ZH',
    '被讯问人摄像机': 'BXWR',
    '讯问人摄像机': 'XWR',
    '卫生间针孔摄像机': 'ZK'
}

all_names = list(name_map.keys())

def getLazyName(x):
    prefix = x['现位置'].replace('普', 'P').replace('智', 'Z').replace('多', 'D')
    lazy_name = name_map[x['设备名称']]
    return f'{prefix}_{lazy_name}'

def getFullName(x):
    prefix = x['现位置']
    full_name = x['设备名称']
    return f'{prefix}_{full_name}'


# 读取数据
ex = pd.read_excel('/Users/louisliu/Downloads/xcjw.xlsx', sheet_name=2)

ex = ex.query(f'设备名称 in {all_names}')

ex['现位置'] = ex['现位置'].ffill()

ex['rtsp'] = ex.apply(lambda x: f'rtsp://admin:xcjw@2024.11@{x["IP地址"]}/id=0', axis=1)
ex['导入后的流ID'] = ex.apply(lambda x: getLazyName(x), axis=1)
ex['name'] = ex.apply(lambda x: getFullName(x), axis=1)
ex['标签'] = None

res = ex[['rtsp','导入后的流ID', 'name', '标签']]
res.rename(columns={'rtsp': '流地址', 'name': '显示名称'}, inplace=True)

res.reset_index(drop=True, inplace=True)

print(res)

res.to_csv(r'xcjuu/import.csv', index=False)
