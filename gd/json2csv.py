import pandas as pd
import numpy as np
import json

ex = pd.read_json('gd/data.json', encoding='utf-8')

grouped = ex.groupby(['所属区域', '二级类目'])

# 最重要生成的map
map = {}
for g in grouped:
    # 一级分类的key
    key = g[0][0]
    value = g[1]
    groupedValue = value.groupby(['二级类目'])
    subMap = {}
    for sub in groupedValue:
        subKey = sub[0][0]
        sub_df = sub[1]
        sub_df_json_str = sub_df.to_json(force_ascii=False, orient='records')
        # ✅ 先解析成 Python 对象（list of dicts）
        sub_df_json = json.loads(sub_df_json_str)
        # 清除值为null的key
        cleaned = [{k: v for k, v in item.items() if v is not None} for item in sub_df_json]
        # 将该二级分类下的列表数据添加到 subMap 中
        subMap[subKey] = cleaned
    if key not in map:
        map[key] = []
    map[key].append(subMap)

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('gd/map.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

# 将map处理成知识库文本
def process_map(map):
    result = []
    for key, value in map.items():
        for subMap in value:# 父分段符
            result.append(f"###main###\n")
            result.append(f"区域: {key}\n")
            for subKey, subValue in subMap.items():
                result.append(f"潜力资源类型: {subKey}\n")
                result.append(f"数量: {len(subValue)}\n")
                # 如果有相关潜力资源数据，加上详情数据
                if len(subValue) > 0:
                    result.append(f"###sub###\n")
                    for subValueItem in subValue:
                        # json转为键值对字符串
                        kv_txt = [", ".join(f"{k}:{v}" for k, v in subValueItem.items())]
                        result.append(f"- {kv_txt}\n")
    return ''.join(result)

dataset_txt = process_map(map)
with open('gd/dataset.txt', 'w', encoding='utf-8') as f:
    f.write(dataset_txt)


