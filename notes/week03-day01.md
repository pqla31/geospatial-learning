# Week 3 · Day 1 —— GeoPandas 入门：GeoDataFrame = DataFrame + geometry 列

上周 pandas 学的四块（表格 / 筛选 / 分组 / 时间序列）今天开始直接变现。

一句话核心：**GeoDataFrame 就是 DataFrame 多带一列 `geometry`**。
属性表、采样台账、站点记录——读进来之后该筛选筛选、该分组分组，上周的所有操作
一个字都不用改。唯一的区别：多了一列存"形状"的列，形状可以是点、线、面。

为什么必须过这一关：下周往后碰 shapefile 属性表，读进来的就是 GeoDataFrame。
pandas 不熟会卡在表操作，今天这步过了，后面只是"多一列"的事。

复用 `week02-pandas/stations.csv` 那 12 行——它们本来就有 lon/lat，
今天把它们变成真正的几何点，画在图上。

时间预算 1.5 小时。

---

## 19_geodataframe_intro.py —— 认识 GeoDataFrame（约 40 分钟）

要求：

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

# ---------- 1. 从零造一个 GeoDataFrame ----------
cities = gpd.GeoDataFrame({
    'name': ['合肥', '宣城', '芜湖'],
    'pop': [963, 250, 380],
    'geometry': [
        Point(117.23, 31.82),
        Point(118.76, 30.94),
        Point(118.38, 31.33),
    ],
})

# ---------- 2. 看 geometry 列 ----------
print(cities.geometry)        # GeoSeries：就是一列 Shapely 对象
print(cities.geometry.x)      # 所有点的经度
print(cities.geometry.y)      # 所有点的纬度

# ---------- 3. pandas 操作全部照用 ----------
print(cities[cities['pop'] > 300])     # 布尔筛选
print(cities['pop'].mean())            # 统计

# ---------- 4. 几何自带属性 ----------
line = LineString([(117, 31), (118, 31), (118, 32)])
poly = Polygon([(117, 31), (118, 31), (118, 32)])
print(line.length)    # 长度
print(poly.area)      # 面积

# ---------- 5. total_bounds：数据覆盖范围 ----------
print(cities.total_bounds)   # [minx, miny, maxx, maxy]
```

要点自查：
- `geometry` 列的类型显示为 `geometry`，单元格里存的是 `POINT (117.23 31.82)`
  这样的 Shapely 对象——不是字符串，也不是两个数字列。这是 GeoDataFrame 和
  DataFrame 的全部区别。
- `Point(经度, 纬度)` —— **x 在前是经度，y 在后是纬度**。这个顺序反了图就飞到
  别的半球，是新手第一坑。
- `line.length` 出来的数不带单位，因为还没说坐标系是什么——单位问题下一节讲。

---

## 20_points_map.py —— 把 stations.csv 变成空间数据（约 50 分钟）

要求：

```python
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 1. 用 pandas 读表（老操作）----------
df = pd.read_csv('week02-pandas/stations.csv')
print(df.dtypes)      # lon/lat 此刻只是普通数字列

# ---------- 2. DataFrame -> GeoDataFrame ----------
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['lon'], df['lat']),
    crs='EPSG:4326',                  # WGS84 经纬度坐标系
)

# 每站在表里有 4 行（4 个月），画图前按站去重，只剩 3 个点
gdf_stations = gdf.drop_duplicates(subset='station')

# ---------- 3. 画出来：表格变地图 ----------
fig, ax = plt.subplots(figsize=(7, 6))
gdf_stations.plot(ax=ax, column='station', legend=True,
                  markersize=100, cmap='tab10')
ax.set_title('三个观测站点的空间分布')
ax.set_xlabel('经度'); ax.set_ylabel('纬度')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('week03-geopandas/stations_map.png', dpi=150)

# ---------- 4. 存成 GeoJSON（GIS 软件能直接打开的格式）----------
gdf_stations.to_file('week03-geopandas/stations.geojson', driver='GeoJSON')
```

要点自查：
- `points_from_xy(经度列, 纬度列)` —— 第一个参数是 lon。写反了三个站会跑到
  非洲去，打开图一眼就能看出来。
- `crs='EPSG:4326'` 是在声明"这些数字是 WGS84 经纬度"。EPSG:4326 是 GPS 和
  绝大多数遥感数据的默认坐标系，先记住这个编号。
- `column='station'` 让每站一个颜色；`legend=True` 出图例——这就是上周
  `groupby` 之外的另一种"按类别区分"的表达方式。
- GeoJSON 是纯文本的 GIS 格式，QGIS / ArcGIS 都能直接打开，可以下载后双击
  丢进 QGIS 看看（选做）。

---

## 验收标准（三条全中才算过）

1. 能说出 GeoDataFrame 和 DataFrame 的区别（多一列 geometry，单元格里是
   Shapely 几何对象），并演示上周的筛选/分组操作在 GeoDataFrame 上原样能跑
2. 能说出 `points_from_xy` 两个参数的顺序含义，以及 EPSG:4326 是什么
3. 生成的 `stations_map.png` 上三个站的位置关系正确：合肥-01 在左上
   （经度最小 117.23、纬度最大 31.82），宣城两站在右下、彼此挨得很近

---

## 收工命令

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week03 day1 练习（GeoDataFrame 入门与站点地图）"
git push
```
