import json
import os
import pandas as pd
import numpy as np

# 数据详情的父子分段，多个子分段，短小精确匹配，父分段是整段内容

if __name__ == "__main__":
    # base_path = 'gd/data_test'
    base_path = 'gd/data20250425143936'
    
    # ########## 脱敏
    # json_str = ''
    # with open(os.path.join(base_path, 'data.json'), 'r', encoding='utf-8') as f:
    #     json_str = f.read()
    
    # json_obj = json.loads(json_str)
    # for o in json_obj:
    #     for k,v in o.items():
    #         if k.find('身份证') > -1 or k.find('姓名') > -1 or k.find('联系方式') > -1 \
    #             or k.find('部门') > -1 or k.find('地理') > -1 or k.find('项目') > -1 or k.find('地址') > -1 \
    #             or k.find('负责') > -1 or k.find('经度') > -1 or k.find('纬度') > -1:
    #             new_v = v[0:2] + '***'
    #             o[k] = new_v

    # json_str = json.dumps(json_obj, ensure_ascii=False)
    # with open(os.path.join(base_path, 'data1.json'), 'w', encoding='utf-8') as f:
    #     f.write(json_str)
    # ########## 脱敏
    
    # 读取源数据到dataframe
    df = pd.read_json(os.path.join(base_path, 'data.json'), encoding='utf-8')

    父级分段符 = f"\n{'*' * 6}\n"
    子级分段符 = f"\n{'-' * 6}\n"
    知识库分段文本列表 = []

    for idx, row in df.iterrows():
        data_map = row.to_dict()
        # 去除空字段，过滤掉之前增加的辅助统计的类型字段(level_x)和最大类型层级字段(max_type_level)
        data_map = {k: v for k, v in data_map.items() if v not in [None, '', np.nan] and not (isinstance(v, float) and np.isnan(v))}
        # 插入总计数据
        知识库分段文本列表.append(json.dumps(data_map, ensure_ascii=False))
        所属区域 = row['所属区域']
        一级类目 = row['一级类目'] 
        二级类目 = row['二级类目'] 
        知识库分段文本列表.append(子级分段符)
        知识库分段文本列表.append(f"@@@{所属区域}-{一级类目}@@@")
        知识库分段文本列表.append(子级分段符)
        知识库分段文本列表.append(f"@@@{所属区域}-{二级类目}@@@")
        知识库分段文本列表.append(父级分段符)

    # 生成的知识库文本
    dataset_txt = ''.join(知识库分段文本列表)

    # 写入文件
    with open(os.path.join(base_path, 'dataset_detailed.txt'), 'w', encoding='utf-8') as f:
        f.write(dataset_txt)

