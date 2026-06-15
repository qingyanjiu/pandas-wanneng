import pandas as pd
import math

df = pd.read_json("/Users/louisliu/dev/AI_projects/pandas-wanneng/ahccs_new_park/camera/jk.json")
df_all = pd.read_csv("/Users/louisliu/dev/通服园区/大华ICC平台接入设备表格/存储相机设备.csv", encoding='gbk', usecols=['通道名称', '地址', '通道号'])

df_all.rename(columns={'通道名称': 'channelName', '地址': 'ip', '通道号': 'channelNum'}, inplace=True)
df_all.dropna(inplace=True)
df_all['channelNum'] = df_all['channelNum'].astype(int)
df_all['channelCode'] = '1000465$1$0$' + (df_all['channelNum'] - 1).astype(str)

df_final = df.merge(df_all, how='inner', left_on='ip', right_on='ip')

df_final.drop(columns=['channelNum'], inplace=True)
print(df_final.head())
df_final.fillna({'name': '未命名监控'}, inplace=True)
df_final.to_json('ahccs_new_park/camera/dahua-list-channelCode-match-3d-code/jk.json', orient='records', force_ascii=False, index=False, indent=2)
df_final.rename(columns={'name': '显示名称', 'source_url': '流地址', 'stream': '导入后的流ID'}, inplace=True)
df_final.to_csv('ahccs_new_park/camera/import.csv', index=False, columns=['流地址', '导入后的流ID', '显示名称'])


