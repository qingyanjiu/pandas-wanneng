import pandas as pd
import pypinyin

df = pd.read_csv(f'/Users/louisliu/dev/AI_projects/pandas-wanneng/hnjuu/监控导入.csv')
df['流地址'] = df["流地址"].apply(lambda x: f"rtsp://admin:Admin123@{x}/id=0;aid=0")
df['导入后的流ID'] = df["显示名称"].apply(lambda x: ''.join([p[0] for p in pypinyin.pinyin(x, style=pypinyin.FIRST_LETTER)]).upper())
df.to_csv(f'/Users/louisliu/dev/AI_projects/pandas-wanneng/hnjuu/监控导入补全后.csv', index=False)