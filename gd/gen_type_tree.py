import json
from collections import defaultdict

def nested_dict():
    return defaultdict(nested_dict)

final_data = nested_dict()
final_data['root'] = {}

# 循环写入map，嵌套，叶子结点的value是空map
def insert_dict(dict, keys):
    current_dict = dict
    for k in keys:
        # 如果这个key不存在，初始化一下下一级dict，然后继续循环，后面会填充下一级的值
        if not k in current_dict.keys():
            current_dict[k] = {}
        current_dict = current_dict[k]

# 嵌套dict转list
def nest_dict_to_list(dict, data_list):
    for k, v in dict.items():
        children = []
        data_list.append({'name': k, 'children': children})
        if not v:
            continue
        else:
            nest_dict_to_list(v, children)

# 读取类型配置文件
types = []
with open('gd/data_test/title_level.json', 'r', encoding='utf-8') as f:
    types = json.loads(f.read())

# 所有节点变成同一级，parents拿出来和最下级分类合并
flat_types = [item['parents'] + [{'name': item['name'], 'level': item['level']}] for item in types]

# 循环所有数据，写入嵌套map
for t in flat_types:
    t.sort(key = lambda x: x['level'])
    keys = [item['name'] for item in t]
    insert_dict(final_data['root'], keys)

data_list = []
nest_dict_to_list(final_data, data_list)

with open('title.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data_list, ensure_ascii=False, indent=4))