import pandas as pd
import numpy as np

df = pd.read_json('/Users/louisliu/dev/AI_projects/pandas-wanneng/anda/zhoujie/zhoujie.json')
df = df.T
df['key'] = df.apply(lambda x: x.name, axis=1)
df = df.drop(columns=['channelId', 'deviceId'])
print(df.head())
df.to_excel('/Users/louisliu/dev/AI_projects/pandas-wanneng/anda/zhoujie/zhoujie.xlsx', index=False)