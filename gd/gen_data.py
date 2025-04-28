import os
import pandas as pd
import json

# 添加缺失的类目信息列
# 一级类目 type_1 二级类目 type_2 三级类目 type_3 依此类推
# max_type_level 表示该数据的最大类目层级
def pre_process_data(df: pd.DataFrame, title_level_map: list, max_level):
    """
    数据预处理
    :param df: 数据frame
    :param type_map: 数据类映射字典
    :return: 处理后的数据框
    """

    ''' 补全缺失的类目信息列, 例如
    {
        "name": "基干民兵",
        "level": 3,
        "parents": [
            {
                "name": "基干民兵222",
                "level": 2
            },
            {
                "name": "人民武装类",
                "level": 1
            }
        ]
    }
    补全后:
    {
        "name": "基干民兵",
        "level": 3,
        "parents": [
            {
                "name": "基干民兵222",
                "level": 2
            },
            {
                "name": "人民武装类",
                "level": 1
            },
            {
                "name": "基干民兵",
                "level": 4
            }
        ]
    }
    '''
    for m in title_level_map:
        # 添加当前类目下级空层级的目录
        for i in range(m['level'] + 1, max_level + 1):
            # 如果没有下级类目，则下级类目的name全都和叶子类目名称一样
            m['parents'].append({
                "name": m['name'],
                "level": i
            })
    
    df.drop('一级类目', axis=1, inplace=True)
    df["max_type_level"] = -1
    # 添加所有空列名，现在都是空值，后面赋值
    for i in range(1, max_level + 1):
        df.insert(i, f"level_{i}", 'Empty')
    # 对每一列进行赋值
    for type_map in title_level_map:
        # 叶子结点数据
        leaf_name = type_map['name']
        # 叶子结点层级
        leaf_level = type_map['level']
        # 其他节点列表
        leaf_parents = type_map['parents']
        # 将叶子类目名称赋值到对应的列
        df.loc[df["二级类目"] == leaf_name, f"level_{leaf_level}"] = leaf_name
        # 将最大层级赋值到对应的列
        df.loc[df["二级类目"] == leaf_name, "max_type_level"] = leaf_level
        # 其他类目名称赋值到对应的列
        for up_level_title in leaf_parents:
            # 插入上级类目的列
            df.loc[df["二级类目"] == leaf_name, f"level_{str(up_level_title['level'])}"] = up_level_title['name']
    # 处理完后，删除二级类目列
    df.drop('二级类目', axis=1, inplace=True)

    # 构造所有区域数据，合并到原数据中
    df_total_area = df.copy()
    df_total_area['所属区域'] = '整个区域'
    df_all = pd.concat([df, df_total_area], ignore_index=True)
    return df_all

# 切分数据集，分别生成知识库文本。然后进行拼接
def do_gen_dataset(dataframe, title_level_map):
    # 循环处理各个级别的数据
    # 总层级的最低的类的层级
    最高层级 = min(list(map(lambda x: x['level'], title_level_map)))
    # 总层级的最高的类的层级
    最低层级 = max(list(map(lambda x: x['level'], title_level_map)))
    # 最高层级数字小，最低层级数字大

    最终知识库文本 = []
    父级分段符 = f"{'*' * 6}\n"
    子级分段符 = f"{'-' * 6}\n"

    for idx, 当前要统计的最低类层级 in enumerate(range(最高层级, 最低层级 + 1)):
        # 查询最高类别层级对应当前层级数的数据，例如所有最高类别为2级的数据，比如 "人防专业队" 数据
        df_with_level:pd.DataFrame = dataframe[dataframe['max_type_level'] == 当前要统计的最低类层级]
        '''
        对每一个数据集分别进行分组统计：
        - 假设如果当前最高类别层级是2，那么就要
        对 index=['所属区域', 'level_1'], columns=['level_2'] 生成透视表，对 level_2 下的数据进行数量统计
        获取 '所属区域'==当前区域，'level_2'==当前类型 的数据列表，作为 level_2 的统计详情
        - 假设如果当前最高类别层级是4，那么就要
        对 index=['所属区域', 'level_1'], columns=['level_4'] 生成透视表，对 level_4 下的数据进行数量统计
        对 index=['所属区域', 'level_2'], columns=['level_4'] 生成透视表，对 level_4 下的数据进行数量统计
        对 index=['所属区域', 'level_3'], columns=['level_4'] 生成透视表，对 level_4 下的数据进行数量统计
        获取 '所属区域'==当前区域，'level_4'==当前类型 的数据列表，作为 level_4 的统计详情
        '''
        # 对当前这一类最高类别层级一致的数据进行分层级groupby统计
        for 要统计的大类层级 in range(1, 当前要统计的最低类层级 + 1):
            # 按区域统计各个层级数据
            # 生成透视表
            pivot = df_with_level.pivot_table(index=['所属区域', f'level_{要统计的大类层级}'], columns=f'level_{当前要统计的最低类层级}', aggfunc='size', fill_value=0)
            # 遍历并计算每行的总计
            for (要统计的区域, 要统计的大类), row in pivot.iterrows():
                # 当前要统计的不是最低类层级，取最低类的详情数据列表
                if 要统计的大类层级 == 当前要统计的最低类层级:
                    最终知识库文本.append(父级分段符)
                    最终知识库文本.append(f"{要统计的区域}{要统计的大类}详情\n")
                    详情数据记录: pd.DataFrame = df_with_level[ \
                        (df_with_level['所属区域'] == 要统计的区域) \
                        & (df_with_level[f'level_{要统计的大类层级}'] == 要统计的大类) \
                    ]
                    data_list = 详情数据记录.to_dict(orient='records')
                    # 去除空字段，过滤掉之前增加的辅助统计的类型字段(level_x)和最大类型层级字段(max_type_level)
                    cleaned_list = [{k: v for k, v in item.items() if (v and pd.notna(v) and 'level' not in k)} for item in data_list]
                    # 插入总计数据
                    最终知识库文本.append(子级分段符)
                    最终知识库文本.append(f'总计: {len(cleaned_list)}\n')
                    # 插入详情数据
                    for 详情数据 in cleaned_list:
                        最终知识库文本.append(子级分段符)
                        最终知识库文本.append(f'{str(详情数据)}\n')
                # 当前要统计的不是最低类层级，取大类下最低类的统计数据
                else:
                    最终知识库文本.append(父级分段符)
                    最终知识库文本.append(f"{要统计的区域}{要统计的大类}统计\n")
                    for 最低层级类名字, 数量 in row.items():
                        if 数量 > 0:
                            最终知识库文本.append(子级分段符)
                            最终知识库文本.append(f'{最低层级类名字}\n')
                            最终知识库文本.append(f'总计{数量}\n')      

    return ''.join(最终知识库文本)

if __name__ == "__main__":
    # base_path = 'gd/data20250425143936'
    base_path = 'gd/data_test'

    # 读取源数据到dataframe
    df = pd.read_json(os.path.join(base_path, 'data.json'), encoding='utf-8')

    # 设置最大类目层级
    max_level = 5

    # 所有叶子类目相关的层级关系
    title_level_map = pd.read_json(os.path.join(base_path, 'title_level.json'), encoding='utf-8').to_dict(orient='records')
    # 预处理，删除一级类目，根据二级类目信息添加实际类目层级,增加一列标识该数据的最大目录层级
    df_all = pre_process_data(df, title_level_map, max_level)
    # 生成的知识库文本
    dataset_txt = do_gen_dataset(df_all, title_level_map)

    # 写入文件
    with open(os.path.join(base_path, 'dataset.txt'), 'w', encoding='utf-8') as f:
        f.write(dataset_txt)

