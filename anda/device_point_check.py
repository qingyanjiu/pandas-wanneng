import pandas as pd
import numpy as np
import os

import re
regex_ABCD = r"['A','B','C','D']"
regex_EFGH = r"['E','F','G','H']"


# 提取建筑信息
def space_build_parent(x: pd.Series):
    extra_area = ''
    if x.loc['area'] == '材料科学大楼':
        if re.match(regex_ABCD, x.loc['build']):
            extra_area = '\\ABCD楼'
        elif re.match(regex_EFGH, x.loc['build']):
            extra_area = '\\EFGH楼'
    return f"{x.loc['type']}{x.loc['area']}{extra_area}"

# 提取楼层点位信息
def space_point_floor_parent(x: pd.Series):
    extra_area = ''
    if x.loc['area'] == '材料科学大楼':
        if re.match(regex_ABCD, x.loc['build']):
            extra_area = 'ABCD楼\\'
        elif re.match(regex_EFGH, x.loc['build']):
            extra_area = 'EFGH楼\\'
    return f"{x.loc['type']}{x.loc['area']}\{extra_area}{x.loc['build']}"

# 提取楼层下房间及走廊点位信息
def space_point_room_parent(x: pd.Series):
    extra_area = ''
    if x.loc['area'] == '材料科学大楼':
        if re.match(regex_ABCD, x.loc['build']):
            extra_area = 'ABCD楼\\'
        elif re.match(regex_EFGH, x.loc['build']):
            extra_area = 'EFGH楼\\'
    return f"{x.loc['type']}{x.loc['area']}\{extra_area}{x.loc['build']}\{x.loc['floor']}"


columns_device = ['device_name', 'device_type_name']
columns_space = ['区域名称（学校、校区、园区）', '建筑名称（楼栋）', '楼层', '点位名称（房间号）']

# 实际文件请查看“示例文件”目录
df_space_qy = pd.read_excel('/Users/louisliu/Desktop/安大-区域点位导入/点位分析/点位.xlsx', sheet_name=0, usecols=lambda c: c in columns_space)
df_space_qy.rename(columns={'区域名称（学校、校区、园区）': 'area', '建筑名称（楼栋）': 'build', '楼层': 'floor', '点位名称（房间号）': 'room'}, inplace=True)
df_space_qy['type'] = '安徽大学\\磬苑校区\\'

df_space_lh = pd.read_excel('/Users/louisliu/Desktop/安大-区域点位导入/点位分析/点位.xlsx', sheet_name=1, usecols=lambda c: c in columns_space)
df_space_lh.rename(columns={'区域名称（学校、校区、园区）': 'area', '建筑名称（楼栋）': 'build', '楼层': 'floor', '点位名称（房间号）': 'room'}, inplace=True)
df_space_lh['type'] = '安徽大学\\龙河校区\\'

df_space = df_space_qy._append(df_space_lh)
df_space.fillna('', inplace=True)

# 拷贝一份dataframe，用于查询
df_space_tmp = df_space.copy()

''' =========================== 建筑查询（点位名称为空，楼层名称为空，但建筑名称不为空） ==========================='''
df_build_tmp = df_space_tmp.query(f'room == "" and floor == "" and build != ""')

df_build = df_build_tmp.copy()
# 点位归属
df_build['parent'] = df_build_tmp.apply(lambda x: space_build_parent(x), axis=1)
# 点位全路径
df_build['full_name'] = df_build_tmp.apply(lambda x: f'{space_build_parent(x)}\{x.loc["build"]}', axis=1)

# 通过点位全路径，对点位去重
df_build.drop_duplicates(subset='full_name', keep='first', inplace=True)
# 保存三级点位数据
df_build.to_excel('/Users/louisliu/Desktop/fb/build.xlsx', index=False)


''' =========================== 1级点位查询（点位名称为空，但楼层名称不为空） ==========================='''
df_space_lv1_tmp = df_space_tmp.query(f'room == "" and floor != ""')

df_space_lv1 = df_space_lv1_tmp.copy()
# 点位归属
df_space_lv1['parent'] = df_space_lv1_tmp.apply(lambda x: space_point_floor_parent(x), axis=1)
# 点位全路径
df_space_lv1['full_name'] = df_space_lv1_tmp.apply(lambda x: f'{space_point_floor_parent(x)}\{x.loc["floor"]}', axis=1)

# 通过点位全路径，对点位去重
df_space_lv1.drop_duplicates(subset='full_name', keep='first', inplace=True)
# 保存三级点位数据
df_space_lv1.to_excel('/Users/louisliu/Desktop/fb/space-lv1-raw.xlsx', index=False)


''' =========================== 2级点位查询（点位名称不为空) ==========================='''
df_space_lv2_tmp = df_space_tmp.query(f'room != ""')

df_space_lv2 = df_space_lv2_tmp.copy()
# 点位归属
df_space_lv2['parent'] = df_space_lv2_tmp.apply(lambda x: space_point_room_parent(x), axis=1)
# 点位全路径
df_space_lv2['full_name'] = df_space_lv2_tmp.apply(lambda x: f'{space_point_room_parent(x)}\{x.loc["room"]}', axis=1)

# 通过点位全路径，对点位去重
df_space_lv2.drop_duplicates(subset='full_name', keep='first', inplace=True)
# 保存三级点位数据
df_space_lv2.to_excel('/Users/louisliu/Desktop/fb/space-lv2.xlsx', index=False)

''' =========================== 1级点位查询（二级点位取一级点位上一级数据生成） ==========================='''

df_space_lv1_tmp = df_space_lv2

df_space_lv1 = df_space_lv1_tmp.copy()
# 点位归属
df_space_lv1['parent'] = df_space_lv1_tmp.apply(lambda x: x.loc['parent'][:x.loc['parent'].rfind('\\')], axis=1)
# 点位全路径
df_space_lv1['full_name'] = df_space_lv1_tmp.apply(lambda x: x.loc['full_name'][:x.loc['full_name'].rfind('\\')], axis=1)

# 通过点位全路径，对点位去重
df_space_lv1.drop_duplicates(subset='full_name', keep='first', inplace=True)
# 保存一级点位数据
df_space_lv1.to_excel('/Users/louisliu/Desktop/fb/space-lv1.xlsx', index=False)

exit(0)
'''================================设备数据整理============================='''
df_device = pd.read_csv('/Users/louisliu/Desktop/安大-区域点位导入/点位分析/iot_device_info.csv', usecols=lambda c: c in columns_device)
# 过滤可以识别的点位名称
df_device_recognizabla = df_device.query('''device_name.str.contains("磬苑") \
                                         or device_name.str.contains("龙河") \
                                         or device_name.str.contains("蜀山") \
                                         or device_name.str.contains("金寨路") \
                                         or device_name.str.contains("大楼")''') 
df_device_unrecognizabla = df_device.query('''not device_name.str.contains("磬苑") \
                                           and not device_name.str.contains("龙河") \
                                           and not device_name.str.contains("蜀山") \
                                           and not device_name.str.contains("金寨路") \
                                           and not device_name.str.contains("大楼")''')

df_device_recognizabla.to_excel('/Users/louisliu/Desktop/fb/device.xlsx', index=False)



