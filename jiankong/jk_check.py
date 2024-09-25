import pandas as pd
import numpy as np

# 读配置文件
ex = pd.read_json('jiankong/jk.json')
# 读数据库中数据
ex1 = pd.read_json('jiankong/data.json')
# 配置文件数据转置
ex = ex.T
# 删除index
ex.reset_index(drop=True, inplace=True)

# stream转成字符串类型
ex['stream'] = ex['stream'].astype(str)
ex1['stream'] = ex1['stream'].astype(str)

# print(ex)
# print(ex1)

# 对配置文件数据做左连接
jk_list = ex.merge(ex1, how='left', left_on='stream', right_on='stream')

# 查询url为空的数据（也就是存在于配置文件中但是不存在于数据库中的记录）
# 再过滤掉ip为空的
# jk_list = jk_list[jk_list['url'].isna()]
jk_list = jk_list.query('url.isna() & ip != ""')

jk_list['rtsp'] = jk_list.apply(lambda x: f'rtsp://admin:wnds1117+@{x["ip"]}:554/cam/realmonitor?channel=1&subtype=1', axis=1)

res = jk_list[['rtsp', 'name_x', 'name_y']]
res.rename(columns={'rtsp': '流地址'}, inplace=True)

res.reset_index(drop=True, inplace=True)

stream_id_start = 110008

# 自动编号，初始编号+下标
res['导入后的流ID'] = res.apply(lambda x: stream_id_start + x.name, axis=1)
res['显示名称'] = res.apply(lambda x: x['name_x'] if x['name_x'] else x['name_y'], axis=1)

res.drop(columns=['name_x', 'name_y'], inplace=True)

res['显示名称'].fillna('未命名', inplace=True)
res['标签'] = ''

print(res)

res.to_csv(r'jiankong/import.csv', index=False)
