import pandas as pd
import math

def gen_stream_name(row):
    num_size = math.floor(math.log(row.name, 10)) + 1 if row.name != 0 else 1
    num_str = '0' * (4 - num_size) + str(row.name)
    return 'jk_zl_{}_{}'.format(row['location'], num_str) if 'f' in row['location'] else 'jk_park_{}'.format(num_str)

exclude_cols = ['位置','监控名字','IP地址','通道名称']

df = pd.read_excel("/Users/louisliu/dev/通服园区/监控点位标注/IP地址（更新版）.xls", sheet_name=0, 
    usecols=lambda c: c in exclude_cols)
df['位置'] = df['位置'].ffill(axis=0)

df.rename(columns={
    '位置': 'location',
    '监控名字': 'name',
    'IP地址': 'ip',
    '通道名称': 'channel_name'
}, inplace=True)

df['name'] = df['location'] + '-' + df['name']
df['source_url'] = 'https://gcalic.v.myalicdn.com/gc/zsslsjjfsd_1/index.m3u8'
df['app'] = 'imported'
df.sort_values(by=['location', 'ip'], inplace=True)

final_df = pd.DataFrame()
locations = df['location'].unique()
for location in locations:
    location_df = df.query('location == @location')
    location_df.reset_index(drop=True, inplace=True)
    location_df['stream'] = location_df.apply(lambda x: gen_stream_name(x), axis=1)
    final_df = pd.concat([final_df, location_df], ignore_index=True)

final_df['space_name'] = final_df['location']

final_df.drop(columns=['location', 'ip', 'channel_name'], inplace=True)

final_df.to_json('ahccs_new_park/camera/jk.json', orient='records', force_ascii=False, index=False, indent=2)

final_df['流地址'] = final_df['source_url']
final_df['导入后的流ID'] = final_df['stream']
final_df['显示名称'] = final_df['name']
final_df.to_csv('ahccs_new_park/camera/import.csv', index=False, columns=['流地址', '导入后的流ID', '显示名称'])

