# Week 3 Day 3 —— 空间连接 sjoin：每个站点落在哪个区里
# 对应任务单：notes/week03-day03.md
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# ---------- 1. 读站点表，变 GeoDataFrame（Day 1 的操作）----------
df = pd.read_csv('week02-pandas/stations.csv')
gdf_points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['lon'], df['lat']),
    crs='EPSG:4326',
)
# 每站 4 个月，画图前按站去重
gdf_stations = gdf_points.drop_duplicates(subset='station').reset_index(drop=True)
print('=== 1. 站点（去重后）===')
print(gdf_stations[['station', 'lon', 'lat', 'geometry']])


# ---------- 2. 建两个行政区多边形 ----------
# 边界是 118.0 经线：合肥 117.23 在西，宣城 118.76/118.81 在东
districts = gpd.GeoDataFrame({
    'district': ['合肥区', '宣城区'],
    'geometry': [
        Polygon([(116.5, 31.5), (118.0, 31.5),
                 (118.0, 32.5), (116.5, 32.5)]),
        Polygon([(118.0, 30.5), (119.5, 30.5),
                 (119.5, 31.5), (118.0, 31.5)]),
    ],
}, crs='EPSG:4326')
print('\n=== 2. 行政区 ===')
print(districts)


# ---------- 3. sjoin：把站点和区连起来 ----------
# predicate='within'：左表的点是否落在右表的多边形内
# how='left'：保留左表所有点，落不进任何区的填 NaN
joined = gpd.sjoin(gdf_stations, districts, how='left', predicate='within')
print('\n=== 3. sjoin 结果（how=left, predicate=within）===')
print(joined[['station', 'lon', 'lat', 'district']])
print()
print('→ 宣城两站 district=宣城区，合肥-01 district=合肥区')
print('  右表 district 列自动接到了左表后面，无后缀（因为列名不冲突）')


# ---------- 4. how='inner' 对比：只保留匹配上的 ----------
joined_inner = gpd.sjoin(gdf_stations, districts, how='inner', predicate='within')
print('\n=== 4. sjoin how=inner（只留匹配上的）===')
print(f'left  行数: {len(joined)}')
print(f'inner 行数: {len(joined_inner)}')
print('→ 本例 3 个点都落进区里，所以 left 和 inner 行数一样')
print('  如果有点落不进任何区，left 会留那行（district=NaN），inner 会丢掉')


# ---------- 5. 出图：点 + 区边界，按所属区着色 ----------
fig, ax = plt.subplots(figsize=(8, 6))
# 先画面边界（底图）
districts.boundary.plot(ax=ax, color='gray', linewidth=1.2)
# 给每个区填浅色
districts.plot(ax=ax, column='district', cmap='Pastel1', alpha=0.5)
# 再画点，按所属区着色
joined.plot(ax=ax, column='district', legend=True,
            markersize=120, cmap='Set1', edgecolor='k')
# 标注站名
for _, row in joined.iterrows():
    ax.annotate(text=row['station'], xy=(row['lon'], row['lat']),
                xytext=(5, 5), textcoords='offset points', fontsize=9)
# 标注区名（取每个区多边形的质心）
for _, row in districts.iterrows():
    c = row.geometry.centroid
    ax.annotate(text=row['district'], xy=(c.x, c.y),
                fontsize=12, ha='center', color='gray')
ax.set_title('站点与行政区空间连接（sjoin）')
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('week03-geopandas/sjoin_map.png', dpi=150)
print('\n图已保存：week03-geopandas/sjoin_map.png')


# ---------- 6. 进阶：把 12 行全表（不去重）sjoin，按区分组算 NDVI 均值 ----------
joined_full = gpd.sjoin(gdf_points, districts, how='left', predicate='within')
print('\n=== 6. 12 行全表 sjoin 后按区分组 NDVI 均值 ===')
print(joined_full.groupby('district')['ndvi'].mean().round(3))
print('→ 这是 sjoin 真正的威力：把"按站分组"升级成"按区分组"')
print('  合肥区只有合肥-01 一个站，宣城区有宣城两站，均值反映了空间聚合')


# ---------- 自己动手 ----------
# 1. 把合肥区东边界从 118.0 改成 117.5，看合肥-01 是否还落在合肥区
# 2. 加一个"芜湖区" Polygon([(118.0, 31.5), (119.5, 31.5), (119.5, 32.5), (118.0, 32.5)])
#    看宣城-02 (118.81, 30.90) 和它是什么关系（应该还是宣城区）
# 3. 改 how='right' 重跑 sjoin，看输出是按区组织还是按点组织
