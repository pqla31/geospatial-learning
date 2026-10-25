"""32_point_extract.py — 矢栅联动第二步：把像元值提取到站点

核心操作：用 src.index(lon, lat) 把 Week 2 的 12 行站点表对到栅格像元，
提取每个站点所在像元的 4 波段值，算卫星 NDVI。

这是"点位观测 vs 像元观测"的尺度对比：
- 站点观测（csv 里的 ndvi）：地面实测，测的是脚下 1 平方米
- 像元观测（栅格提取）：卫星观测，一个像元覆盖 5.6 km × 5.6 km
两者必然有差异 —— 这就是遥感"尺度效应"的实例。
"""
import numpy as np
import pandas as pd
import rasterio
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

# ---------- 1. 读站点表 + 栅格 ----------
df = pd.read_csv('week02-pandas/stations.csv')
src = rasterio.open('week04-rasterio/sample.tif')

print('=== 站点表（12 行）===')
print(df[['station', 'lon', 'lat', 'ndvi']].to_string(index=False))
print(f'\n栅格像元尺寸: {src.transform.a} 度 × {-src.transform.e} 度 ≈ 5.6 km')

# ---------- 2. 每行站点提取像元值 ----------
blues, greens, reds, nirs, raster_ndvis = [], [], [], [], []
for _, row in df.iterrows():
    lon, lat = row['lon'], row['lat']
    r, c = src.index(lon, lat)                       # 经纬度 → 像元号
    b, g, red, nir = src.read()[:, r, c]             # 4 波段值
    ndvi_pixel = (nir - red) / (nir + red)            # 卫星 NDVI

    blues.append(b); greens.append(g); reds.append(red)
    nirs.append(nir); raster_ndvis.append(ndvi_pixel)

df['blue']  = np.round(blues, 3)
df['green'] = np.round(greens, 3)
df['red']   = np.round(reds, 3)
df['nir']   = np.round(nirs, 3)
df['raster_ndvi'] = np.round(raster_ndvis, 3)

src.close()

# ---------- 3. 对比站点观测 vs 卫星像元 ----------
print('\n=== 站点观测 vs 卫星像元 NDVI ===')
print(df[['station', 'date', 'ndvi', 'raster_ndvi']].to_string(index=False))

print('\n→ csv 的 ndvi 是站点月际观测（0.12-0.75），raster_ndvi 是卫星空间观测')
print('  两者体系不同（非同时相、非同传感器），差异体现尺度效应 —— 不要求一致')

# ---------- 4. 按站分组看地物类型 ----------
print('\n=== 按站分组：像元波段值揭示地物类型 ===')
station_summary = df.groupby('station').agg(
    obs_ndvi=('ndvi', 'mean'),
    raster_ndvi=('raster_ndvi', 'mean'),
    nir=('nir', 'mean'),
    red=('red', 'mean'),
).round(3)
print(station_summary)

print('\n→ 看 NIR 判断地物：')
print('  合肥-01 NIR ≈ 0.23 → 城市像元（NIR 低）')
print('  宣城-01/02 NIR ≈ 0.45 → 植被像元（NIR 高）')
print('  同一站 4 个月的 raster_ndvi 完全一样 —— 因为卫星只拍了 1 次单时相')


# ---------- 自己动手 ----------
# 1. 给每个站点周围 3×3 像元取均值（而不是单像元），算 raster_ndvi_3x3，
#    对比单像元 vs 3×3 均值 —— 3×3 更能代表站点周边地物，减少单像元噪声
# 2. 站点落在水体上的话 raster_ndvi 会是负值。stations.csv 里没有水站点，
#    手动加一行"巢湖站 (117.5, 31.9)"，看它提取出来的 raster_ndvi 是不是负的
# 3. 算 12 行的 obs_ndvi 和 raster_ndvi 的相关系数（df['ndvi'].corr(df['raster_ndvi'])），
#    很低是正常的（一个看时间、一个看空间），理解为什么不能直接比
