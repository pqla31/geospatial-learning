"""31_mask_raster.py — 矢栅联动第一步：用矢量裁栅格

核心操作：用 Week 3 的行政区 shapefile 裁 Week 4 的遥感影像，
每个区算一个 NDVI 均值 —— 这就是"分区统计"（zonal stats）。

矢栅联动铁律：矢量和栅格 CRS 必须一致才能 mask。
Week 3 的 districts.shp 是 4326，sample.tif 也是 4326，正好对上。
"""
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)   # 屏蔽 GDAL_DATA 警告

# ---------- 1. 读矢量 + 栅格 ----------
districts = gpd.read_file('week03-geopandas/shp/districts.shp')
src = rasterio.open('week04-rasterio/sample.tif')

print('=== CRS 一致性检查 ===')
print(f'  矢量 districts.shp crs: {districts.crs.to_epsg()}')
print(f'  栅格 sample.tif   crs: {src.crs.to_epsg()}')
assert districts.crs.to_epsg() == src.crs.to_epsg(), 'CRS 不一致，必须先统一'
print('  → CRS 一致，可以 mask')

# ---------- 2. 按区裁栅格 + 算 NDVI 均值 ----------
print('\n=== 分区 NDVI 统计 ===')
results = []
for idx, row in districts.iterrows():
    name = row['区名']
    geom = [row['geometry']]                        # mask 要传几何列表

    # mask: crop=True 裁到区的边界框，区外设 nodata
    out_arr, out_transform = mask(src, geom, crop=True, nodata=-9999)

    # 算 NDVI
    red, nir = out_arr[2], out_arr[3]
    with np.errstate(invalid='ignore', divide='ignore'):
        ndvi = (nir - red) / (nir + red)

    # 排除 nodata 像元（区外被设成 -9999 的不能算）
    valid = ndvi[ndvi != -9999]
    mean_ndvi = float(valid.mean())
    n_pixels = valid.size

    results.append({'区名': name, 'ndvi_mean': round(mean_ndvi, 3),
                    '像元数': n_pixels})
    print(f'  {name}: NDVI 均值 {mean_ndvi:.3f}, 有效像元 {n_pixels}')

src.close()

# ---------- 3. 结果表 ----------
result_df = pd.DataFrame(results)
print('\n=== 分区统计结果 ===')
print(result_df.to_string(index=False))
print('\n→ 合肥区含城市+水体（NDVI 接近 0 或负），宣城区含植被（NDVI 正）')


# ---------- 自己动手 ----------
# 1. 把合肥区几何往南扩 0.5 度（用 shapely.buffer 或手动改坐标），
#    看它吃进水体区后 NDVI 均值怎么变 —— 几何改了统计就变，这是空间敏感性的实例
# 2. 用 src.read() 全读 + 布尔掩膜（不用 mask）手算一个区的均值：
#    生成"像元中心点 within 区"的布尔矩阵，拿它当掩膜算 NDVI 均值，
#    对比 mask 的结果一不一样（应该一样，但 mask 更高效）
# 3. 把每个区的裁剪结果写成单独的 tif（用 rasterio.open 'w' + out_transform），
#    这样每个区有独立影像文件 —— 实战里"按行政区切分影像"就这么干
