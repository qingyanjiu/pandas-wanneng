import pandas as pd
import numpy as np
import json

# 点位dataframe - UE上点位名称 IP
point_df = pd.read_excel('/Users/louisliu/dev/AI_projects/pandas-wanneng/menjin/point.xlsx', sheet_name='门禁问题', usecols=lambda c: c != '升级情况' and c!= '问题' and c!= '楼层', skiprows=1)

point_df.rename(columns={
    '名称': 'pointName', 
    '位置': 'position', 
    'ip地址': 'ip', 
    '用户名账号': 'username',
    '密码': 'password'
    }, inplace=True)

# point_df.ffill(inplace=True)
point_df.fillna('', inplace=True)

# 设备dataframe - 设备名称 IP
device_cols = ['*设备名称', '*设备类型', '设备IP', '通道数']
device_df = pd.read_excel('/Users/louisliu/dev/AI_projects/pandas-wanneng/menjin/device.xlsx', sheet_name=0, usecols=lambda c: c in (device_cols), skiprows=0)
device_df.rename(columns={
    '*设备名称': 'deviceName', 
    '*设备类型': 'type', 
    '设备IP': 'ip', 
    '通道数': 'channelNumber'
    }, inplace=True)

# print(device_df.head(5))

# 通道json - 设备名称 通道编号 通道code
channel_df = pd.read_json('/Users/louisliu/dev/AI_projects/pandas-wanneng/menjin/channel.json', encoding='utf-8')
# print(channel_df.head(5))


# 点位与设备进行右连接
p_d_left_df = point_df.merge(device_df, how='right', left_on='ip', right_on='ip')
# print(p_d_left_df.head(5))

# 再与通道进行左连接
p_d_left_c_df = p_d_left_df.merge(channel_df, how='left', left_on='deviceName', right_on='deviceName')

p_d_left_c_df.drop(['workMode', 'status', 'orgCode', 'deviceModel', 'escFlag', 'flag', 'onlineStatus'], axis=1, inplace=True)
p_d_left_c_df.fillna('0', inplace=True)
p_d_left_c_df['channelSeq'] = p_d_left_c_df['channelSeq'].astype(int)
p_d_left_c_df['deviceCode'] = p_d_left_c_df['deviceCode'].astype(int)



map = {}
for index, row in p_d_left_c_df.iterrows():
    # 门禁控制器通道编号
    seq = row.loc['channelSeq']
    key = row.loc['pointName']
    deviceType = row.loc['type']
    if (deviceType == '集中控制器'):
        key = key[0:len(key) - 1] + str(seq + 1)
    map[key] = row.iloc[1:].to_dict()

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('/Users/louisliu/dev/AI_projects/pandas-wanneng/menjin/mj_all.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)
