import pandas as pd
import numpy as np
import json

ex = pd.read_excel('/home/coder/project/pandas/iot.xls', sheet_name=2)

grouped = ex.groupby(['name'])

map = {}
for g in grouped:
    key = g[0][0]
    value = g[1]
    groupedValue = value.groupby(['pointName'])
    subMap = {}
    for sub in groupedValue:
        subKey = sub[0][0]
        subValue = sub[1].iloc[0].to_json(force_ascii=False)
        subMap[subKey] = json.loads(subValue)
    map[key] = subMap

print(map)

mapStr = json.dumps(map, ensure_ascii=False)
        
with open('iot.json', 'w', encoding='utf-8') as f:
    f.write(mapStr)

