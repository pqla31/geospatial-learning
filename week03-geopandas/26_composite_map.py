# Week 3 Day 4 —— 综合出图：把三天的技能串成一条流程
# 读 shapefile → sjoin 聚合 → 重投影 → buffer → 分级填色出图
# 对应任务单：notes/week03-day04.md
import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# ---------- 1. 读 shapefile（昨天存好的）----------
# 如果还没跑 25 生成 shp，先跑 25
shp_dir = 'week03-geopandas/shp'
if not os.path.exists(os.path.join(shp_dir, 'districts.shp')):
    print('请先运行 25_shapefile_io.py 生成 shapefile')
    raise SystemExit

districts = gpd.read_file(os.path.join(shp_dir, 'districts.shp'))
stations = gpd.read_file(os.path.join(shp_dir, 'stations.shp'))
print('=== 1. 读回 shapefile ===')
print(f'行政区: {len(districts)} 个   站点: {len(stations)} 个')
print(f'CRS: {districts.crs.to_epsg()}')


# ---------- 2. sjoin：站点落哪个区（Day 3 技能）----------
# how='left' 保留所有站点，predicate='within' 点在区内
joined = gpd.sjoin(stations, districts, how='left', predicate='within')
print('\n=== 2. sjoin 后 ===')
print(joined[['站名', 'ndvi', '区名']])


# ---------- 3. 按区聚合 NDVI 均值（Day 2 groupby + Day 3 sjoin）----------
# 把站点的 NDVI 通过 sjoin 带到区上，再按区分组
district_ndvi = joined.groupby('区名')['ndvi'].mean().round(3)
print('\n=== 3. 每区 NDVI 均值 ===')
print(district_ndvi)

# 把均值写回 districts（普通 merge，按区名连）
districts = districts.merge(
    district_ndvi.reset_index().rename(columns={'ndvi': 'ndvi_mean'}),
    on='区名',
    how='left',
)
print('\n=== 3. 区表加上 ndvi_mean 列 ===')
print(districts[['区名', 'ndvi_mean']])


# ---------- 4. 重投影到米坐标系（Day 2 技能）----------
# 画图可以在 4326，但 buffer 必须在投影坐标系
districts_m = districts.to_crs('EPSG:3857')
stations_m = stations.to_crs('EPSG:3857')
joined_m = joined.to_crs('EPSG:3857')


# ---------- 5. 站点 5km buffer（Day 2 技能）----------
station_buffer = stations_m.copy()
station_buffer['geometry'] = stations_m.geometry.buffer(5000)   # 5000 米 = 5 公里
print('\n=== 5. 站点 5km buffer 面积 ===')
print((station_buffer.geometry.area / 1e6).round(2).tolist(), 'km²')


# ---------- 6. 综合出图：四层叠图 ----------
fig, ax = plt.subplots(figsize=(9, 7))

# 层 1：行政区按 NDVI 均值分级填色（matplotlib 自动分箱）
districts_m.plot(ax=ax, column='ndvi_mean', cmap='RdYlGn',
                 legend=True, legend_kwds={'label': 'NDVI 均值'},
                 edgecolor='k', linewidth=1, alpha=0.7)

# 层 2：站点 5km buffer 半透明圆
station_buffer.plot(ax=ax, color='none', edgecolor='blue',
                    linewidth=1.5, alpha=0.6)

# 层 3：站点本身（实心点）
stations_m.plot(ax=ax, color='red', markersize=60, zorder=5)

# 层 4：站名标注
for _, row in joined_m.iterrows():
    ax.annotate(text=row['站名'], xy=(row.geometry.x, row.geometry.y),
                xytext=(6, 6), textcoords='offset points', fontsize=9)

# 区名标注（取质心）
for _, row in districts_m.iterrows():
    c = row.geometry.centroid
    ax.annotate(text=f"{row['区名']}\nNDVI {row['ndvi_mean']:.2f}",
                xy=(c.x, c.y), fontsize=11, ha='center',
                color='black', fontweight='bold')

ax.set_title('综合图：行政区 NDVI 分级 + 站点 5km 缓冲区')
ax.set_xlabel('X (米, Web Mercator)')
ax.set_ylabel('Y (米)')
ax.grid(alpha=0.3)

# 手动补 buffer 图例（geopandas 多边形 label 不进图例，Day 2 学过的坑）
handles, _ = ax.get_legend_handles_labels()
handles.append(Patch(facecolor='none', edgecolor='blue', label='站点 5km 缓冲区'))
ax.legend(handles=handles, loc='upper right')

fig.tight_layout()
fig.savefig('week03-geopandas/composite_map.png', dpi=150)
print('\n图已保存：week03-geopandas/composite_map.png')
print('\n=== 流程回顾 ===')
print('1. read_file 读 shapefile     ← 今天学的')
print('2. sjoin 站点落区             ← Day 3')
print('3. groupby 按区聚合 NDVI      ← Day 2 + Day 3')
print('4. to_crs 重投影到米          ← Day 2')
print('5. buffer 5km 缓冲区          ← Day 2')
print('6. plot column 分级填色       ← Day 1 + matplotlib')
print('→ 这就是 GIS 工程的标准流程：点数据 → 空间聚合 → 面统计 → 可视化')


# ---------- 自己动手 ----------
# 1. 把 buffer 改成 10km，看缓冲区是否开始重叠（宣城两站相距约 5km）
# 2. 换 cmap='YlGn'（黄到绿，适合植被），看 NDVI 填色变化
# 3. 加一个 joined.groupby('区名')['ndvi'].std() 算每区 NDVI 标准差，
#    标注成"NDVI 均值±标准差"，看哪个区内部差异大
