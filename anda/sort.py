import pandas as pd
import numpy as np
import os

columns = ['设备名称', '设备串号', '区域/建筑', '楼层', '现房间号', 'code']

ex = pd.read_excel('/Users/louisliu/dev/AI_projects/pandas-wanneng/anda/1.xls', sheet_name=1, usecols=lambda c: c in columns)
ex.rename(columns={'设备名称': 'build', '区域/建筑': 'domain', '楼层': 'floor', '现房间号': 'name', '设备串号': 'id'}, inplace=True)

build_names = ex.groupby(['build']).agg({'build': pd.Series.nunique}).to_dict()
build_name_list = list(build_names['build'].keys())

for i in build_name_list:
    df_build = ex.query(f'build == "{i}"')
    df_build.sort_values(by='floor', ascending=True)
    new_df_build = pd.DataFrame()
    # 楼层列赋值
    new_df_build = df_build.copy()
    new_df_build['domain'] = df_build.apply(lambda x: x.loc['domain'].replace(i, i[5:] + '\\' + x.loc['name'][:x.loc['name'].find('F') + 1]), axis=1).copy()
    new_df_build.to_excel(os.path.join('/Users/louisliu/dev/AI_projects/pandas-wanneng/anda', f'{i}.xlsx'), index=False)
