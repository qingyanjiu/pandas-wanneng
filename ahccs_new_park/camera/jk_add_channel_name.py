import pandas as pd
import math

df = pd.read_json("/Users/louisliu/dev/AI_projects/pandas-wanneng/ahccs_new_park/camera/jk.json")
df_all = pd.read_json("/Users/louisliu/dev/AI_projects/pandas-wanneng/ahccs_new_park/camera/all.json")
list = df_all.data.units[0]['channels']
df_all = pd.DataFrame(list)
df_all['channelDeviceIp'] = df_all['chExt'].apply(lambda x: x['channelDeviceIp'])
df_ext = df_all[['channelName', 'channelDeviceIp']]
df_final = df.merge(df_ext, how='left', left_on='ip', right_on='channelDeviceIp')
df_final['name'] = df_final['channelName']
df_final.drop(columns=['channelName', 'channelDeviceIp'], inplace=True)
print(df_final.head())
df_final.to_json('ahccs_new_park/camera/jk_add_channel.json', orient='records', force_ascii=False, index=False, indent=2)
df_final.rename(columns={'name': '显示名称', 'source_url': '流地址', 'stream': '导入后的流ID'}, inplace=True)
df_final.to_csv('ahccs_new_park/camera/import.csv', index=False, columns=['流地址', '导入后的流ID', '显示名称'])


