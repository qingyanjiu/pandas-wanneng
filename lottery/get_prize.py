import pandas as pd
import math

include_cols = ['姓名', '身份证', '奖品', '奖项']

df = pd.read_excel("lottery/副本中奖名单(3).xlsx", sheet_name=0, 
    usecols=lambda c: c in include_cols)
df['奖品'] = df['奖品'].ffill(axis=0)

df.rename(columns={
    '姓名': 'name',
    '身份证': 'id_card',
    '奖品': 'prize_name',
    '奖项': 'prize'
}, inplace=True)

print(df.head(5))

df.to_excel('lottery/整理后名单.xlsx', index=False)

for i in range(1, 5):
    sub_df = df.query(f'prize == {i}')
    mapping = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth'
    }
    prize_name = mapping[i]
    sub_df.to_json(f'lottery/{mapping[i]}-prize.json', orient='records', force_ascii=False, index=False, indent=2)


