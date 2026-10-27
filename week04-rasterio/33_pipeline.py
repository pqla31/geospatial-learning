"""33_pipeline.py — 学期项目收口：NDVI 计算 + 分区统计完整流程

把 Week 1-4 学的全部串成一条流程，出两张综合图：
  pipeline_map.png   — NDVI 栅格底图 + 行政区边界 + 站点标注（主成果图）
  pipeline_stats.png — 分区 NDVI 对比 + 站点观测 vs 卫星像元

流程回顾（每步对应哪周学的）：
  1. 读遥感影像 sample.tif          ← Week 4 Day 1 rasterio
  2. 算 NDVI 栅格 (nir-red)/(nir+red) ← Week 1 NumPy 公式
  3. 读行政区 districts.shp          ← Week 3 geopandas
  4. 分区统计 NDVI 均值 (mask)       ← Week 4 Day 3 矢栅联动
  5. 站点像元提取                    ← Week 4 Day 3 + Week 2 站点表
  6. 出综合图                        ← Week 1 matplotlib + Week 3 叠图
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 1. 读三类数据 ----------
src = rasterio.open('week04-rasterio/sample.tif')
districts = gpd.read_file('week03-geopandas/shp/districts.shp')
stations = pd.read_csv('week02-pandas/stations.csv')

print('数据加载:')
print(f'  栅格: {src.width}x{src.height}, {src.count} 波段, crs={src.crs.to_epsg()}')
print(f'  矢量: {len(districts)} 个区, crs={districts.crs.to_epsg()}')
print(f'  站点: {len(stations)} 行, {stations["station"].nunique()} 个站')

# ---------- 2. 算 NDVI 栅格 ----------
arr = src.read()
ndvi_raster = (arr[3] - arr[2]) / (arr[3] + arr[2])
left, bottom, right, top = src.bounds

# ---------- 3. 分区统计 ----------
zone_stats = []
for _, row in districts.iterrows():
    out, _ = mask(src, [row['geometry']], crop=True, nodata=-9999)
    z_ndvi = (out[3] - out[2]) / (out[3] + out[2])
    valid = z_ndvi[z_ndvi != -9999]
    zone_stats.append({
        '区名': row['区名'],
        'ndvi_mean': round(float(valid.mean()), 3),
        '像元数': valid.size,
    })
zone_df = pd.DataFrame(zone_stats)
print('\n分区统计:')
print(zone_df.to_string(index=False))

# ---------- 4. 站点像元提取 ----------
station_pts = stations.drop_duplicates('station').reset_index(drop=True)
extracted = []
for _, s in station_pts.iterrows():
    r, c = src.index(s['lon'], s['lat'])
    b, g, red, nir = arr[:, r, c]
    extracted.append({
        'station': s['station'], 'lon': s['lon'], 'lat': s['lat'],
        'raster_ndvi': round((nir - red) / (nir + red), 3),
        'nir': round(float(nir), 3),
    })
extract_df = pd.DataFrame(extracted)
print('\n站点像元提取:')
print(extract_df.to_string(index=False))
src.close()

# ---------- 5. 图1：综合地图 ----------
fig, ax = plt.subplots(figsize=(10, 7))

# NDVI 栅格底图
im = ax.imshow(ndvi_raster, cmap='RdYlGn', vmin=-1, vmax=1,
               extent=(left, right, bottom, top), alpha=0.7)
fig.colorbar(im, ax=ax, label='NDVI', shrink=0.7)

# 行政区边界叠图
districts.boundary.plot(ax=ax, color='black', linewidth=1.5)
for _, row in districts.iterrows():
    centroid = row['geometry'].centroid
    zone_ndvi = zone_df[zone_df['区名'] == row['区名']]['ndvi_mean'].values[0]
    ax.annotate(f"{row['区名']}\nNDVI {zone_ndvi:.3f}",
                xy=(centroid.x, centroid.y),
                fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='black', alpha=0.8))

# 站点标注
colors = {'合肥-01': '#d62728', '宣城-01': '#1f77b4', '宣城-02': '#ff7f0e'}
for _, s in extract_df.iterrows():
    ax.scatter(s['lon'], s['lat'], c=colors.get(s['station'], 'black'),
               s=80, edgecolor='white', zorder=5)
    ax.annotate(s['station'], xy=(s['lon'], s['lat']),
                xytext=(8, 8), textcoords='offset points', fontsize=9)

ax.set_title('NDVI 空间分布 + 行政区分区统计 + 站点位置', fontsize=13)
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
legend_elements = [mpatches.Patch(facecolor=c, edgecolor='white', label=k)
                   for k, c in colors.items()]
ax.legend(handles=legend_elements, loc='upper left', title='站点')
fig.tight_layout()
fig.savefig('week04-rasterio/pipeline_map.png', dpi=150)
print('\n图1已存: pipeline_map.png')

# ---------- 6. 图2：统计对比 ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左：分区 NDVI 柱状图
bar_colors = ['#d62728' if v < 0.3 else '#2ca02c' for v in zone_df['ndvi_mean']]
ax1.bar(zone_df['区名'], zone_df['ndvi_mean'], color=bar_colors)
ax1.set_title('分区 NDVI 均值对比')
ax1.set_ylabel('NDVI 均值')
ax1.set_ylim(-0.2, 0.8)
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.grid(alpha=0.3, axis='y')

# 右：站点观测 vs 卫星像元
obs = stations.groupby('station')['ndvi'].mean().reindex(extract_df['station'])
sat = extract_df.set_index('station')['raster_ndvi']
x = np.arange(len(extract_df))
w = 0.35
ax2.bar(x - w/2, obs.values, w, label='站点观测均值', color='#4a90d9')
ax2.bar(x + w/2, sat.values, w, label='卫星像元 NDVI', color='#2e8b57')
ax2.set_xticks(x)
ax2.set_xticklabels(extract_df['station'])
ax2.set_title('站点观测 vs 卫星像元 NDVI')
ax2.set_ylabel('NDVI')
ax2.legend()
ax2.grid(alpha=0.3, axis='y')

fig.tight_layout()
fig.savefig('week04-rasterio/pipeline_stats.png', dpi=150)
print('图2已存: pipeline_stats.png')

print('\n=== 学期项目收口完成 ===')
print('Week 1-4 流程全部串通：')
print('  栅格读取 → NDVI 计算 → 矢量裁剪 → 分区统计 → 站点提取 → 综合出图')


# ---------- 自己动手 ----------
# 1. 把这张 pipeline_map.png 放进 README（用 ![标题](week04-rasterio/pipeline_map.png)），
#    让别人点进仓库首页就能看到学期项目成果
# 2. 加一个"裸土区"多边形（南部城市和植被之间的过渡带），
#    算它的 NDVI 均值，看是不是介于合肥区和宣城区之间
# 3. 把流程封装成函数 ndvi_pipeline(tif_path, shp_path, csv_path)，
#    换一份真实数据（网上下个 Sentinel-2 小块 + 行政边界）直接能跑 —— 这就是可复用工具
