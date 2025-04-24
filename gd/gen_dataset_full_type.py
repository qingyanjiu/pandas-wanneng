import pandas as pd
import numpy as np
import json
from collections import defaultdict

# 添加缺失的类目信息列
# 一级类目 type_1 二级类目 type_2 三级类目 type_3 叶子类目 type_leaf
def pre_process_data(df: pd.DataFrame, type_maps: list, max_level):
    """
    数据预处理
    :param df: 数据frame
    :param type_map: 数据类映射字典
    :return: 处理后的数据框
    """
    # 删除一级类目列
    df.drop('一级类目', axis=1, inplace=True)
    # 叶子类目列名
    max_level_col_name = f"level_{max_level}"
    # 将二级类目列名改为 level_最大类目层级
    df.rename(columns={"二级类目": max_level_col_name}, inplace=True)
    for type_map in type_maps:
        leaf_name = type_map['name']
        leaf_parents = type_map['parents']
        for up_level_titile in leaf_parents:
            # 插入上级类目的列
            df.loc[df[max_level_col_name] == leaf_name, f"level_{str(up_level_titile['level'])}"] = up_level_titile['name']



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

# 将map处理成各区域中一级分类下二级数据的知识库文本
def process_map(data):
    # 所有一级的key，都是区域名称，找出来后面需要用到
    all_area_names = data.keys()
    result = []

    # 递归处理map
    def recursive_process(node, path, area_info):
        if isinstance(node, list):
            full_path = ''.join(path)
            # 叶子节点：打印资源详情
            result.append("******\n")
            result.append(f"{full_path}资源\n")
            result.append("------\n")
            result.append(f"总计: {len(node)}\n")
            for item in node:
                result.append("------\n")
                kv_txt = ','.join(f"{k}: {v}" for k, v in item.items())
                result.append(f"{kv_txt}\n")
            # 到本个mapitem的末尾，下面是区域信息
            # 走到最后一层(list)，说明这里肯定是最低级的类目了，打个标签，让生成文本的时候不要进行该类目的统计（因为最低一级类目有详情信息）
            area_info['is_leaf_type'] = True
            return f"{path[-1]}\n总计: {len(node)}\n"
        elif isinstance(node, dict):
            # 中间节点：递归处理
            summary = ''
            for key, value in node.items():
                # 如果当前key是区域名称，且区域和上一个区域不一致，重新设置当前区域信息
                if key in all_area_names and key != area_info['current_area']:
                    area_info['current_area'] = key

                # 分段标题，如果key是现在是当前区域，则不拼接区域信息在前面（防止出现拼接出来"承德市承德市资源"）
                path = [area_info['current_area']] + [key] if key not in all_area_names else [key]
                sub_summary = recursive_process(value, path, area_info)
                summary += sub_summary
                # summary = sub_summary
                # path长度大于0，且不包含"Empty"的节点，且不是叶子类目(叶子类目不需要做数量统计，只需要详情)，说明是一个有效的区域 
                if len(path) > 0 and 'Empty' not in path and not area_info['is_leaf_type']:
                    result.append("******\n")
                    result.append(f"{''.join(path)}资源\n")
                    result.append("------\n")
                    result.append(summary)
                # 一次递归走完，下一个节点肯定不是叶子类目
                area_info['is_leaf_type'] = False
            return summary
        else:
            return ''

    recursive_process(data, [], {"current_area": "", "is_leaf_type": False})
    return ''.join(result)


def do_gen_dataset(dataframe, max_level, title_level_map):
    # 将缺失的类目层级添加到map中,保证生成完整的列
    for m in title_level_map:
        # 算出当前类目最大类型层级比最大层级少多少
        level_offset = max_level - m['level']
        m['level'] = m['level'] + level_offset
        # 所有的上级类目都要加上这个偏移量
        for l in m['parents']:
            l['level'] = l['level'] + level_offset
        # 将不存在的类目的列的值设为Empty
        for i in range(1, level_offset + 1):
            # 如果没有下级类目，则下级类目的name全都和叶子类目名称一样
            m['parents'].append({
                "name": 'Empty',
                "level": i
            })

    # 预处理，删除一级类目，根据二级类目信息添加实际类目层级
    pre_process_data(dataframe, title_level_map, max_level)
    # 测试数据
    # dataframe = dataframe.loc[dataframe['level_4'] == '人防指挥所']

    # 根据总层级，生成按每一个层级分组的map
    # 按区域、1234类目层级分组的map
    area_map = gen_group_map(dataframe=dataframe, groupby_cols=['所属区域', 'level_1', 'level_2', 'level_3', 'level_4'])
    # 按大类小类分组的全部数据map，套在“整个区域”中
    all_map = gen_group_map(dataframe=dataframe, groupby_cols=['level_1', 'level_2', 'level_3', 'level_4'])

    area_map['全部区域'] = all_map

    # 保存map到json文件
    map_str = json.dumps(area_map, ensure_ascii=False)
    with open('gd/map1.json', 'w', encoding='utf-8') as f:
        f.write(map_str)

    dataset_txt = process_map(area_map)
    return dataset_txt

if __name__ == "__main__":
    # 读取源数据到dataframe
    df = pd.read_json('gd/data.json', encoding='utf-8')
    # 设置最大类目层级
    max_level = 4
    # 类目映射信息
    # title_level_map = [
    #     {
    #         "name": "基干民兵",
    #         "level": 3,
    #         "parents": [
    #             {
    #                 "name": "基干民兵222",
    #                 "level": 2
    #             },
    #             {
    #                 "name": "人民武装类",
    #                 "level": 1
    #             }
    #         ]
    #     }
    # ]
    # 所有叶子类目相关的层级关系
    title_level_map = pd.read_json('gd/title_level.txt', encoding='utf-8').to_dict(orient='records')
    # 生成的知识库文本
    dataset_txt = do_gen_dataset(df, max_level, title_level_map)
    # 写入文件
    with open('gd/dataset.txt', 'w', encoding='utf-8') as f:
        f.write(dataset_txt)

