"""29_reproject.py — 栅格重投影：4326 → 3857

栅格重投影 = 把像元重新铺到另一个坐标系的网格上。
和 Week 3 矢量 to_crs 的区别：矢量只要换坐标，栅格要重新切分像元网格，
所以像元数会变、像元值会变（插值产生新值）。

本练习把 sample.tif 从 EPSG:4326（经纬度，单位度）重投影到 EPSG:3857（Web Mercator，单位米）。
"""
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

src = rasterio.open('week04-rasterio/sample.tif')

# ---------- 1. 算目标网格的 transform 和尺寸 ----------
# calculate_default_transform 自动按目标 CRS 切分像元网格
dst_crs = 'EPSG:3857'
dst_transform, dst_width, dst_height = calculate_default_transform(
    src.crs, dst_crs, src.width, src.height, *src.bounds
)

print('=== 源栅格（EPSG:4326，单位度）===')
print(f'  transform  : {src.transform}')
print(f'  bounds     : {tuple(round(b, 3) for b in src.bounds)}')
print(f'  像元尺寸   : {src.transform.a} 度 × {-src.transform.e} 度')
print(f'  shape      : ({src.height}, {src.width})')

print('\n=== 目标栅格（EPSG:3857，单位米）===')
print(f'  transform  : {dst_transform}')
print(f'  像元尺寸   : {dst_transform.a:.0f} 米 × {-dst_transform.e:.0f} 米')
print(f'  shape      : ({dst_height}, {dst_width})')
print(f'  → 像元数从 {src.width*src.height} 变成 {dst_width*dst_height}，'
      f'因为 4326 在 31°N 处 1 度经度≈95km、1 度纬度≈111km，3857 要重新切网格')

# ---------- 2. 重投影 ----------
# 4 波段都重投影。反射率是连续值，用 bilinear（双线性插值）；
# 分类图（如土地覆盖）才用 nearest（最近邻，不产生新类别）
dst = np.zeros((src.count, dst_height, dst_width), dtype=src.dtypes[0])
for i in range(1, src.count + 1):
    reproject(
        source=rasterio.band(src, i),
        destination=dst[i - 1],
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.bilinear,
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
with rasterio.open('week04-rasterio/sample_3857.tif', 'w', **profile) as f:
    f.write(dst)
    f.descriptions = src.descriptions
print('已写入 sample_3857.tif')

# ---------- 4. 对比源/目标的 NDVI ----------
src_arr = src.read()
src_ndvi = (src_arr[3] - src_arr[2]) / (src_arr[3] + src_arr[2])
dst_ndvi = (dst[3] - dst[2]) / (dst[3] + dst[2])

print('\n=== NDVI 对比（重投影前后）===')
print(f'  源 (4326) : range [{src_ndvi.min():.3f}, {src_ndvi.max():.3f}]  mean {src_ndvi.mean():.3f}')
print(f'  目标(3857): range [{dst_ndvi.min():.3f}, {dst_ndvi.max():.3f}]  mean {dst_ndvi.mean():.3f}')
print('  → bilinear 插值会让极值略缩（-1.0 可能变成 -0.98），但分布基本一致')

# ---------- 5. 读回 sample_3857.tif 自检 ----------
with rasterio.open('week04-rasterio/sample_3857.tif') as r:
    print(f'\n=== sample_3857.tif 自检 ===')
    print(f'  crs    : {r.crs.to_epsg()}')
    print(f'  bounds : {tuple(round(b, 0) for b in r.bounds)} (单位: 米)')
    print(f'  像元   : {r.transform.a:.0f} m × {-r.transform.e:.0f} m')
    print(f'  bands  : {r.count}, descriptions: {r.descriptions}')

src.close()
print('\n29 完成。下一题：30 窗口读取。')


# ---------- 自己动手 ----------
# 1. 把 resampling 改成 Resampling.nearest，重跑看 NDVI 范围是不是和源完全一致
#    （nearest 不插值，值原样搬，分类图必须用 nearest 防止产生不存在的新类别）
# 2. 试着重投影到 EPSG:32651（UTM 51N），看像元尺寸和 3857 有什么不同
#    （UTM 在中纬度更精确，3857 在高纬变形严重——这是 Web 地图用 3857、专业量算用 UTM 的原因）
# 3. 算一下 4326 的 0.05 度像元在 31°N 处实际多大（经度方向 ≈ 0.05 × 95 = 4.75km），
#    和 3857 的像元尺寸对比，理解为什么"度用来定位、米用来量算"
