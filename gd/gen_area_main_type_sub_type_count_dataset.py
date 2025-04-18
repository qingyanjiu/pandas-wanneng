import pandas as pd
import numpy as np
import json
from collections import defaultdict

ex = pd.read_json('gd/data.json', encoding='utf-8')
ex.sort_values(by=['所属区域', '一级类目', '二级类目'], inplace=True, ignore_index=True)

map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for _, row in ex.iterrows():
    area = row["所属区域"]
    fclass = row["一级类目"]
    sclass = row["二级类目"]
    row_json = json.loads(row.to_json(force_ascii=False, orient='index'))
    # 清除值为null的key
    cleaned = {k: v for k, v in row_json.items() if v}
    map[area][fclass][sclass].append(cleaned)

mapStr = json.dumps(map, ensure_ascii=False)
        
# with open('gd/map1.json', 'w', encoding='utf-8') as f:
#     f.write(mapStr)


# 将map处理成各区域中一级分类下二级数据的知识库文本
# def process_map(map):
#     # 主_子分段文本数据
#     result = []
#     for areaKey, areaValue in map.items():
#         for fKey, fValue in areaValue.items():
#             result.append(f"###main###\n")
#             result.append(f"区域: {areaKey}\n")
#             result.append(f"潜力资源类型: {fKey}\n")
#             result.append(f"数量: {len(fValue)}\n")
#             result.append(f"###sub###\n")
#             for sKey, sValue in fValue.items():
#                 result.append(f"潜力资源子类型: {sKey}\n")
#                 result.append(f"数量: {len(sValue)}\n")
#                 for tValue in sValue:
#                     # 如果有相关潜力资源数据，加上详情数据
#                     if len(sValue) > 0:
#                         kv_txt = ''
#                         for k, v in tValue.items():
#                             # json转为键值对字符串
#                             kv_txt += f"{k}: {v},"
#                         result.append(f"- {kv_txt}\n")
#     return ''.join(result)


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
                            # json转为键值对字符串
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

dataset_txt = process_map(map)
with open('gd/dataset1.txt', 'w', encoding='utf-8') as f:
    f.write(dataset_txt)