import requests
import fiona
from shapely.geometry import mapping
import os
from shapely.geometry import Polygon


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://yncx.mnr.gov.cn",
    "Referer": "https://yncx.mnr.gov.cn/yn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "^sec-ch-ua": "^\\^Not/A)Brand^^;v=^\\^8^^, ^\\^Chromium^^;v=^\\^126^^, ^\\^Microsoft",
    "sec-ch-ua-mobile": "?0",
    "^sec-ch-ua-platform": "^\\^Windows^^^"
}
url = "https://yncx.mnr.gov.cn/7H8i9J0k1L2m3N4o5p6Q7R8s9T0u1V2w3X4y5Z6/queryResults.json"
params = {
    "returnContent": "true"
}

form_data = {
    'queryMode': 'SpatialQuery',
    'queryParameters': {
        'customParams': None,
        'prjCoordSys': {'epsgCode': 4490},
        'expectCount': 1000,
        'networkType': "LINE",
        'queryOption': "ATTRIBUTEANDGEOMETRY",
        'queryParams': [{'name': "pro31@yndk", 'attributeFilter': "1=1", 'fields': None}],
        'startRecord': 0,
        'holdTime': 10,
        'returnCustomResult': False,
        'returnFeatureWithFieldCaption': False
    },
    'geometry': {
        'id': 0,
        'style': None,
        'parts': [5],
        'points': [
            {'id': "SuperMap.Geometry_1", 'bounds': None, 'SRID': None, 'x': 120.70459, 'y': 32.41937, 'tag': None, 'type': "Point", 'geometryType': "Point"},
            {'id': "SuperMap.Geometry_2", 'bounds': None, 'SRID': None, 'x': 120.70731, 'y': 32.41935, 'tag': None, 'type': "Point", 'geometryType': "Point"},
            {'id': "SuperMap.Geometry_3", 'bounds': None, 'SRID': None, 'x': 120.70727, 'y': 32.41797, 'tag': None, 'type': "Point", 'geometryType': "Point"},
            {'id': "SuperMap.Geometry_4", 'bounds': None, 'SRID': None, 'x': 120.70459, 'y': 32.41802, 'tag': None, 'type': "Point", 'geometryType': "Point"},
            {'id': "SuperMap.Geometry_5", 'bounds': None, 'SRID': None, 'x': 120.70459, 'y': 32.41937, 'tag': None, 'type': "Point", 'geometryType': "Point"}
        ],
        'type': "REGION",
        'prjCoordSys': {'epsgCode': None}
    },
    'spatialQueryMode': "INTERSECT"
}


response = requests.post(url, headers=headers, params=params, json=form_data)
jsondata=response.json()
features=jsondata["recordsets"][0]["features"]

# 保存文件路径
file_path='yjnt.geojson'

# 检查文件是否存在，如果不存在则创建文件并写入初始数据
if not os.path.exists(file_path):
    with fiona.open(file_path, 'w', driver='GeoJSON', crs='EPSG:4490', schema={'geometry': 'Polygon', 'properties': {'ID': 'int'}}) as file:
        for item in features:
            polygon = Polygon([(coord['x'], coord['y']) for coord in item['geometry']['points']])
            file.write({
                'properties': {'ID': item['ID']},
                'geometry': mapping(polygon),
            })

else:
    # 读取已有数据的ID列表
    existing_ids = []
    with fiona.open(file_path, 'r') as file:
        for feature in file:
            existing_ids.append(feature['properties']['ID'])

    # 打开GeoJSON文件以追加模式写入
    with fiona.open(file_path, 'a') as file:
        # 遍历每组坐标数据
        for item in features:
            if item['ID'] not in existing_ids:
                polygon = Polygon([(coord['x'], coord['y']) for coord in item['geometry']['points']])
                file.write({
                    'properties': {'ID': item['ID']},
                    'geometry': mapping(polygon),
                })