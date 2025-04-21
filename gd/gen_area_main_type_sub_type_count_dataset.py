import pandas as pd
import numpy as np
import json
from collections import defaultdict

# 根据传入的列名列表动态进行分组，返回嵌套map
def gen_dynamic_level_map(dataframe: pd.DataFrame, groupby_cols: list, current_level: int):
    """
    递归生成动态分级map
    :param dataframe: 数据框
    :param groupby_cols: 分组列
    :param current_level: 当前级别
    :return: map
    """
    if current_level >= len(groupby_cols):
        df_json_str = dataframe.to_json(force_ascii=False, orient='records')
        # ✅ 先解析成 Python 对象（list of dicts）
        df_json = json.loads(df_json_str)
        # 清除值为null的key
        cleaned = [{k: v for k, v in item.items() if v} for item in df_json]
        return cleaned

    # 获取当前级别的列名
    current_col = groupby_cols[current_level]

    # 按当前级别分组
    grouped = dataframe.groupby(current_col)

    # 递归处理每个组
    result = {}
    for name, group in grouped:
        result[name] = gen_dynamic_level_map(group, groupby_cols, current_level + 1)

    return result

# 根据动态列从dataframe中生成嵌套map
def gen_group_map(dataframe: pd.DataFrame, groupby_cols: list):
    # 排序 
    dataframe.sort_values(by=groupby_cols, inplace=True, ignore_index=True)
    # 递归生成maps
    map = gen_dynamic_level_map(dataframe, groupby_cols, 0)
    return map

# 根据区域，类目生成嵌套map
# def gen_area_map(dataframe):
#     dataframe.sort_values(by=['所属区域', '一级类目', '二级类目'], inplace=True, ignore_index=True)

#     map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

#     for _, row in dataframe.iterrows():
#         area = row["所属区域"]
#         fclass = row["一级类目"]
#         sclass = row["二级类目"]
#         row_json = json.loads(row.to_json(force_ascii=False, orient='index'))
#         # 清除值为null以及值为空的key
#         cleaned = {k: v for k, v in row_json.items() if v}
#         map[area][fclass][sclass].append(cleaned)

#     return map


# 将map处理成各区域中一级分类下二级数据的知识库文本
def process_map(map):
    # 主_子分段文本数据
    result = []
    for areaKey, areaValue in map.items():
        for fKey, fValue in areaValue.items():
            sValueCountStr = ''
            for sKey, sValue in fValue.items():
                # 主分段分隔符
                result.append(f"******\n")
                # result.append(f"{areaKey}资源\n") #TODO 增加详情字眼
                # result.append(f"###sub###\n")
                # result.append(f"{fKey} - 数量: {len(fValue)}\n")  #TODO 去掉一级类信息，后面有统计信息
                # 子分段分隔符
                # result.append(f"------\n")
                result.append(f"{areaKey}{sKey}资源\n")   #TODO 二级类详情字眼
                # 子分段分隔符
                result.append(f"------\n")
                result.append(f"总计: {len(sValue)}\n")
                for tValue in sValue:
                    # 子分段分隔符
                    result.append(f"------\n")
                    # 如果有相关潜力资源数据，加上详情数据
                    if len(sValue) > 0:
                        kv_txt = ''
                        for k, v in tValue.items():
                            # if k in [
                            #         "姓名", "身份证号码", "性别", "民族", "政治面貌", "文化程度", "户口所在地",
                            #         "家庭住址", "本人联系方式", "主要亲属姓名", "主要亲属联系方式", "工作单位详细名称",
                            #         "工作单位详细地址", "工作单位联系方式", "是否为退役军人", "分队编码", "分队名称",
                            #         "队伍级别", "力量类型", "专业", "职务", "专业是否对口", "是否为参训对象", "采集批次号",
                            #         "地理位置", "机构名称"
                            #         ]:
                            #     kv_txt += f'{k}: "",'
                            # else:
                            #     # json转为键值对字符串
                            #     kv_txt += f"{k}: {v},"
                            kv_txt += f"{k}: {v},"
                        result.append(f"{kv_txt}\n")
                sValueCountStr += f"{sKey}\n"
                sValueCountStr += f"总计: {len(sValue)}\n" 
                # 子分段分隔符
                sValueCountStr += f"------\n"
            # 主分段分隔符
            result.append(f"******\n")
            result.append(f"{areaKey}{fKey}资源 \n")
            # 子分段分隔符
            result.append(f"------\n")
            result.append(f"{sValueCountStr}")
    return ''.join(result)



df = pd.read_json('gd/data.json', encoding='utf-8')
# 按区域、大类、小类分组的map
area_map = gen_group_map(dataframe=df, groupby_cols=['所属区域', '一级类目', '二级类目'])

# 按大类小类分组的全部数据map，套在“整个区域”中
all_map = gen_group_map(dataframe=df, groupby_cols=['一级类目', '二级类目'])

area_map['全部区域'] = all_map

# 保存map到json文件
# map_str = json.dumps(area_map, ensure_ascii=False)
# with open('gd/map1.json', 'w', encoding='utf-8') as f:
#     f.write(map_str)

dataset_txt = process_map(area_map)
with open('gd/dataset.txt', 'w', encoding='utf-8') as f:
    f.write(dataset_txt)