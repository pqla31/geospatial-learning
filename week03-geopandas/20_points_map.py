# Week 3 Day 1 —— 把 stations.csv 变成真正的空间数据
# 对应任务单：notes/week03-day01.md
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# ---------- 1. 用 pandas 读表（老操作）----------
df = pd.read_csv('week02-pandas/stations.csv')
print('--- 此刻 lon/lat 只是普通数字列 ---')
print(df.dtypes)


# ---------- 2. DataFrame -> GeoDataFrame：一步之差 ----------
# points_from_xy(经度, 纬度) —— 第一个参数是 lon，别反！
# crs='EPSG:4326' 声明这些数字是 WGS84 经纬度（GPS 默认坐标系）
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['lon'], df['lat']),
    crs='EPSG:4326',
)
print('\n--- 变成 GeoDataFrame 后 ---')
print(gdf.dtypes)
print('CRS:', gdf.crs.to_epsg())


# ---------- 3. 每站 4 行（4 个月），画图前按站去重 ----------
# drop_duplicates 也是上周 pandas 的操作
gdf_stations = gdf.drop_duplicates(subset='station').reset_index(drop=True)
print('\n--- 去重后 ---')
print(gdf_stations[['station', 'lon', 'lat', 'geometry']])


# ---------- 4. 画出来：表格变地图 ----------
# column='station'：按站点着色；legend=True：出图例
fig, ax = plt.subplots(figsize=(7, 6))
gdf_stations.plot(ax=ax, column='station', legend=True,
                  markersize=100, cmap='tab10')
ax.set_title('三个观测站点的空间分布')
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('week03-geopandas/stations_map.png', dpi=150)
print('\n图已保存：week03-geopandas/stations_map.png')


# ---------- 5. 存成 GeoJSON ----------
# 纯文本 GIS 格式，QGIS / ArcGIS 都能直接打开
gdf_stations.to_file('week03-geopandas/stations.geojson', driver='GeoJSON')
print('GeoJSON 已保存：week03-geopandas/stations.geojson')


# ---------- 自己动手 ----------
# 1. 把 markersize 改成 300，看点变大后三站的相对位置是不是更清楚
# 2. ax.set_xlim(116, 120); ax.set_ylim(30, 33) 手动设定范围，对比默认范围
# 3. 给 gdf 加一列 gdf['ndvi_mean'] = gdf.groupby('station')['ndvi'].transform('mean')
#    再用 column='ndvi_mean' 画图——颜色代表 NDVI 均值而不是站点
