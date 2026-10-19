# Week 3 Day 4 —— Shapefile 读写：GIS 工业的通用格式
# 对应任务单：notes/week03-day04.md
import os
import geopandas as gpd
from shapely.geometry import Point, Polygon


# ---------- 1. 先造数据：两个区 + 三个站点 ----------
# 字段名故意用短中文（≤3 字）—— 长中文字段名会崩，后面第 4 步专门演示
districts = gpd.GeoDataFrame({
    '区名': ['合肥区', '宣城区'],
    'geometry': [
        Polygon([(116.5, 31.5), (118.0, 31.5),
                 (118.0, 32.5), (116.5, 32.5)]),
        Polygon([(118.0, 30.5), (119.5, 30.5),
                 (119.5, 31.5), (118.0, 31.5)]),
    ],
}, crs='EPSG:4326')

stations = gpd.GeoDataFrame({
    '站名': ['宣城-01', '宣城-02', '合肥-01'],
    'lon': [118.76, 118.81, 117.23],
    'lat': [30.94, 30.90, 31.82],
    'ndvi': [0.60, 0.56, 0.49],   # 各站 4 个月均值（简化）
    'geometry': [
        Point(118.76, 30.94),
        Point(118.81, 30.90),
        Point(117.23, 31.82),
    ],
}, crs='EPSG:4326')


# ---------- 2. 写 shapefile：一个 .shp 变成 5 个文件 ----------
os.makedirs('week03-geopandas/shp', exist_ok=True)
districts.to_file('week03-geopandas/shp/districts.shp', driver='ESRI Shapefile')
stations.to_file('week03-geopandas/shp/stations.shp', driver='ESRI Shapefile')

print('=== 2. 写完后看文件列表 ===')
for f in sorted(os.listdir('week03-geopandas/shp')):
    print(f'  {f}')
print()
print('→ 一个 districts.shp 实际是 5 个文件：')
print('  .shp  几何数据（点的坐标/面的顶点）')
print('  .shx  空间索引（快速查找用）')
print('  .dbf  属性表（区名、ndvi 这些列）')
print('  .prj  坐标系定义（EPSG:4326 写在里面）')
print('  .cpg  编码声明（告诉读的人用 UTF-8，中文才不乱）')
print('→ 5 个文件缺一不可，拷给别人要打包整个文件夹')


# ---------- 3. 读回来验证中文 ----------
d_back = gpd.read_file('week03-geopandas/shp/districts.shp')
s_back = gpd.read_file('week03-geopandas/shp/stations.shp')
print('\n=== 3. 读回 districts.shp ===')
print(d_back)
print('\n=== 3. 读回 stations.shp ===')
print(s_back)
print(f'\nCRS: {d_back.crs.to_epsg()}   ← .prj 文件起的作用')
print('→ 中文区名/站名正常，因为 .cpg 声明了 UTF-8 编码')


# ---------- 4. 坑：长中文字段名会崩 ----------
# shapefile 的 .dbf 字段名限制 10 字节，中文 UTF-8 占 3 字节/字
# 所以中文字段名最多 3 个字（9 字节），第 4 个字就超限
print('\n=== 4. 坑演示：长中文字段名 ===')
print('  "区名"     = 2 字 = 6 字节  OK')
print('  "行政区名" = 4 字 = 12 字节  超 10 字节限制，写 .shp 会崩')
print('  → 想用长中文字段名？换 GeoJSON，没这个限制')
print('  → 或者字段名用英文（station/district），值用中文没问题')


# ---------- 5. 对比：同样数据存 GeoJSON ----------
districts.to_file('week03-geopandas/shp/districts.geojson', driver='GeoJSON')
print('\n=== 5. 同样数据存 GeoJSON ===')
print(f'  GeoJSON 单文件: {os.path.getsize("week03-geopandas/shp/districts.geojson")} 字节')
print(f'  Shapefile 5 文件总计: {sum(os.path.getsize(os.path.join("week03-geopandas/shp",f)) for f in os.listdir("week03-geopandas/shp") if f.startswith("districts"))} 字节')
print('→ GeoJSON 一个 .json 文件，文本格式，能直接打开看')
print('  Shapefile 5 个二进制文件，必须用 GIS 软件读')
print('  两种都是 GIS 通用格式，QGIS/ArcGIS 都能开')


# ---------- 自己动手 ----------
# 1. 用记事本打开 districts.geojson，看 JSON 结构（coordinates 里就是顶点坐标）
# 2. 把 stations.shp 的"站名"列改成"观测站点名称"（6 字），跑一下看报什么错
# 3. 删掉 .cpg 文件再读 districts.shp，看中文会不会乱（提示：可能乱也可能不乱，取决于读取引擎）
