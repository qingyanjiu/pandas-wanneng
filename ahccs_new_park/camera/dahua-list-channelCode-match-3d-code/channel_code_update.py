import pandas as pd
import math
'''
将导出表格中的监控编码换成我们打点的code
'''


def gen_jk_code(row):
    if row['设备楼层内ID'] != None:
        num_size = math.floor(math.log(row['设备楼层内ID'], 10)) + 1 if row['设备楼层内ID'] != 0 else 1
        num_str = '0' * (4 - num_size) + str(row['设备楼层内ID'])
        return 'jk_zl_{}_{}'.format(row['位置'].lower(), num_str) if 'f' in row['位置'] else 'jk_park_{}'.format(num_str)
    return ''

def gen_mj_code(row):
    if row['设备楼层内ID'] != None:
        num_size = math.floor(math.log(row['设备楼层内ID'], 10)) + 1 if row['设备楼层内ID'] != 0 else 1
        num_str = '0' * (4 - num_size) + str(row['设备楼层内ID'])
        return 'mj_zl_{}_{}'.format(row['位置'].lower(), num_str)
    return ''
    
df = pd.read_excel("/Users/louisliu/dev/通服园区/设备台账/jk_all.xls")
df_all = pd.read_excel("/Users/louisliu/dev/通服园区/点位标注/设备ip-4-30-已打code.xlsx", sheet_name=0)
df_all = df_all.dropna(subset=['设备楼层内ID'])
df_all['设备楼层内ID'] = df_all['设备楼层内ID'].astype(int)
df_all['位置'] = df_all['位置'].ffill(axis=0)
df_all['code'] = df_all.apply(lambda x: gen_jk_code(x), axis=1)

print(df.head())

df_final = df.merge(df_all, how='left', left_on='IP地址', right_on='IP地址')

df['设备编号'] = df_final['code']

df.sort_values(by='设备编号', na_position='first', inplace=True)
df = df.drop_duplicates(subset=['IP地址'])



df.to_excel('jk_all.xlsx', index=False)


