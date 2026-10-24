"""29_reproject.py — 栅格重投影：4326 → UTM 50N (32650)

栅格重投影 = 把像元重新铺到另一个坐标系的网格上。
和 Week 3 矢量 to_crs 的区别：矢量只要换坐标，栅格要重新切分像元网格，
所以像元数会变、像元值会变（插值产生新值）。

本练习把 sample.tif 从 EPSG:4326（经纬度，单位度）重投影到 EPSG:32650（UTM 50N，单位米）。
自选练习：resampling 改成 nearest 验证极值不变；UTM 带从 51N 修正为 50N（117°E 是 50N 中央经线）。
"""
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

src = rasterio.open('week04-rasterio/sample.tif')

# ---------- 1. 算目标网格的 transform 和尺寸 ----------
# calculate_default_transform 自动按目标 CRS 切分像元网格
# UTM 分带：每 6 度一带，117°E 是 50N 的中央经线（数据在 116.5-119.5E → 用 32650）
# 32651 = UTM 51N 中央经线 123°E，数据离它太远会变形 + easting 出负值
dst_crs = 'EPSG:32650'
dst_transform, dst_width, dst_height = calculate_default_transform(
    src.crs, dst_crs, src.width, src.height, *src.bounds
)

print('=== 源栅格（EPSG:4326，单位度）===')
print(f'  transform  : {src.transform}')
print(f'  bounds     : {tuple(round(b, 3) for b in src.bounds)}')
print(f'  像元尺寸   : {src.transform.a} 度 × {-src.transform.e} 度')
print(f'  shape      : ({src.height}, {src.width})')

print(f'\n=== 目标栅格（EPSG:{dst_crs.split(":")[1]}，单位米）===')
print(f'  transform  : {dst_transform}')
print(f'  像元尺寸   : {dst_transform.a:.0f} 米 × {-dst_transform.e:.0f} 米')
print(f'  shape      : ({dst_height}, {dst_width})')
print(f'  → 像元数从 {src.width*src.height} 变成 {dst_width*dst_height}，'
      f'因为 {dst_crs.split(":")[1]} 要重新切网格')

# ---------- 2. 重投影 ----------
# 自选：用 nearest（最近邻）——不插值，极值和源完全一致。
# 反射率标准做法是 bilinear（双线性），但分类图必须 nearest 防止产生不存在的新类别。
dst = np.zeros((src.count, dst_height, dst_width), dtype=src.dtypes[0])
for i in range(1, src.count + 1):
    reproject(
        source=rasterio.band(src, i),
        destination=dst[i - 1],
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )

print(f'\n重投影完成，输出数组 shape: {dst.shape}')

# ---------- 3. 写成新 tif ----------
profile = src.profile.copy()
profile.update({
    'crs': dst_crs,
    'transform': dst_transform,
    'width': dst_width,
    'height': dst_height,
})
with rasterio.open('week04-rasterio/sample_reproject.tif', 'w', **profile) as f:
    f.write(dst)
    f.descriptions = src.descriptions
print('已写入 sample_reproject.tif')

# ---------- 4. 对比源/目标的 NDVI ----------
src_arr = src.read()
src_ndvi = (src_arr[3] - src_arr[2]) / (src_arr[3] + src_arr[2])
dst_ndvi = (dst[3] - dst[2]) / (dst[3] + dst[2])

dst_epsg = dst_crs.split(':')[1]
print('\n=== NDVI 对比（重投影前后）===')
print(f'  源 (4326)     : range [{src_ndvi.min():.3f}, {src_ndvi.max():.3f}]  mean {src_ndvi.mean():.3f}')
print(f'  目标({dst_epsg}): range [{dst_ndvi.min():.3f}, {dst_ndvi.max():.3f}]  mean {dst_ndvi.mean():.3f}')
print('  → nearest 不插值，极值和源完全一致（vs bilinear 会缩到 -0.902）')

# ---------- 5. 读回 sample_reproject.tif 自检 ----------
with rasterio.open('week04-rasterio/sample_reproject.tif') as r:
    print(f'\n=== sample_reproject.tif 自检 ===')
    print(f'  crs    : {r.crs.to_epsg()}')
    print(f'  bounds : {tuple(round(b, 0) for b in r.bounds)} (单位: 米)')
    print(f'  像元   : {r.transform.a:.0f} m × {-r.transform.e:.0f} m')
    print(f'  bands  : {r.count}, descriptions: {r.descriptions}')

src.close()
print('\n29 完成。下一题：30 窗口读取。')


# ---------- 自己动手 ----------
# 1. [已完成] resampling 改成 Resampling.nearest → 极值 [-1.0, 0.809] 和源完全一致
#    （nearest 不插值，分类图必须用 nearest 防止产生不存在的新类别）
# 2. [已完成] UTM 带：51N(32651) → 50N(32650)。
#    117°E 是 UTM 50N 的中央经线，数据在 116.5-119.5E 属 50N 带；
#    用 51N 会 easting 出负值（-124396），50N 围绕 500000 波动才对。
# 3. 算一下 4326 的 0.05 度像元在 31°N 处实际多大（经度方向 ≈ 0.05 × 95 = 4.75km），
#    和 UTM 的 5006 米对比，理解为什么"度用来定位、米用来量算"
