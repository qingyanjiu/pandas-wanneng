# 将表格中转换2000投影坐标转换到地理坐标
from pyproj import Transformer
import pandas as pd

def do_transform_cord(x, y):
    """
    将投影坐标转换为地理坐标（经纬度）
    
    参数:
    x: 投影坐标的东向分量（单位：米）
    y: 投影坐标的北向分量（单位：米）
    
    返回:
    (lon, lat): 转换后的经度和纬度
    """
    # 使用 pyproj 创建一个从投影坐标系（CGCS2000 高斯-克吕格 3°带）转 WGS84 经纬度的转换器
    # 以117°为中央经线（3度带，带号=117/3 + 1 = 40）
    proj_str = "+proj=tmerc +lat_0=0 +lon_0=117 +k=1 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs"
    
    transformer = Transformer.from_proj(proj_str, "EPSG:4326", always_xy=True)
    
    lon, lat = transformer.transform(x, y)
    return lon, lat

if __name__ == '__main__':
    df = pd.read_excel('/Users/louisliu/dev/济南堤口果品批发市场/数据采集/堤口监控位点清单.xlsx', 
                        sheet_name=0, header=0)
    df.fillna('0', inplace=True)
    new_cord = df.apply(lambda row: do_transform_cord(float(row['X坐标']), float(row['Y坐标'])), axis=1, result_type='expand')
    df[['lon', 'lat']] = new_cord
    # 删除列
    df.drop(columns=['序号', '远程通道号', '加密'], inplace=True)
    # 重命名列
    df.rename(columns={
        'IP地址': 'ip',
        '端口': 'port',
        '厂商': 'manufacturer',
        '用户名': 'username',
        '密码': 'password',
        '通道名称': 'name',
        '机号': 'nvr',
        'X坐标': 'x',
        'Y坐标': 'y',
        '相对高度': 'z',
        '朝向（正北方向为0度，顺时针计算角度）': 'direction',
        '备注': 'remark',
    }, inplace=True)
    df.to_json('/Users/louisliu/dev/济南堤口果品批发市场/数据采集/jk.json', orient='records', force_ascii=False, indent=4)
    print('转换完成')   