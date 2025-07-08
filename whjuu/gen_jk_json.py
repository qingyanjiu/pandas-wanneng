import pandas as pd
import json

df = pd.read_excel('/Volumes/elements-bk/BM-DATA/whjw/摄像头-1区-整理后.new.xlsx', sheet_name=0, header=0)
df.ffill(inplace=True)
df.drop(columns=['房间', '序号', '数量', 'app'], inplace=True)
df.rename(columns={'设备': 'name'}, inplace=True)
df.set_index('stream', inplace=True)

df.to_json('whjuu/jk.json', indent=4, orient='index', index=True, force_ascii=False)