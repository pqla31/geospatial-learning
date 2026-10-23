"""27_rasterio_intro.py — rasterio 入门：读 tif、认识栅格数据结构

栅格 = 像元的矩阵 + 地理坐标信息（transform/CRS）。
和 Week 1 NumPy 数组的区别：NumPy 只有数字，rasterio 的栅格知道"每个像元对应地面哪里"。

本练习的 sample.tif 必须先存在——先跑 gen_sample_tif.py 生成。
"""
import numpy as np
import rasterio

src = rasterio.open('week04-rasterio/sample.tif')

# ---------- 1. 元数据：栅格的"身份证" ----------
print('=== 栅格元数据 ===')
print(f'count    (波段数): {src.count}')
print(f'width    (列数)  : {src.width}')
print(f'height   (行数)  : {src.height}')
print(f'dtypes           : {src.dtypes}')
print(f'crs      (坐标系): {src.crs.to_epsg()}')
print(f'transform        : {src.transform}')
print(f'bounds   (范围)  : {tuple(round(b, 3) for b in src.bounds)}')
print(f'nodata           : {src.nodata}')
print(f'descriptions    : {src.descriptions}')
print(f'shape = (bands, height, width) = ({src.count}, {src.height}, {src.width})')

# ---------- 2. transform：像元号 ↔ 地理坐标 的换算表 ----------
# Affine 对象是 3×3 矩阵，关键 4 个属性：
#   .a = 像元宽度（经度方向），.e = -像元高度（行向下增 → 纬度向下减）
#   .c = 左上角经度，.f = 左上角纬度
a, e, c, f = src.transform.a, src.transform.e, src.transform.c, src.transform.f
print('\n=== transform 解读 ===')
print(f'像元宽 {a} 度 ≈ {a * 111:.1f} km（经度方向）')
print(f'像元高 {-e} 度 ≈ {-e * 111:.1f} km（纬度方向）')
print(f'左上角中心坐标: ({c + a/2:.3f}, {f + e/2:.3f})')

# ---------- 3. 逐波段读 ----------
print('\n=== 逐波段统计 ===')
for i in range(1, src.count + 1):
    band = src.read(i)   # 单波段读 → 2D 数组 (height, width)
    name = src.descriptions[i - 1]
    print(f'band {i} {name:>5}: min={band.min():.3f} max={band.max():.3f} '
          f'mean={band.mean():.3f} shape={band.shape}')

# ---------- 4. 坐标 → 像元号：把站点对到像元 ----------
# 合肥-01 站点坐标（Week 2 那张表）
lon, lat = 118.76, 30.94
row, col = src.index(lon, lat)    # 经纬度 → 行列号
print(f'\n=== 站点采样 ===')
print(f'宣城-01 ({lon}, {lat}) 落在 row={row}, col={col}')
val = src.read()[:, row, col]      # 该像元 4 波段值
print(f'该像元 4 波段值: B={val[0]:.3f} G={val[1]:.3f} R={val[2]:.3f} NIR={val[3]:.3f}')

# ---------- 5. 像元号 → 坐标（反向）----------
lon2, lat2 = src.xy(row, col)     # 像元中心坐标
print(f'该像元中心坐标: ({lon2:.4f}, {lat2:.4f})')
print(f'该像元左上角: {src.transform * (col, row)}')   # transform 可像函数一样调用

# ---------- 6. 读全部波段 + 算 NDVI 栅格 ----------
arr = src.read()                  # (4, 40, 60) — (波段, 行, 列)
red, nir = arr[2], arr[3]
ndvi = (nir - red) / (nir + red)
print(f'\n=== NDVI 栅格 ===')
print(f'shape={ndvi.shape}, range [{ndvi.min():.3f}, {ndvi.max():.3f}]')
print(f'整景 NDVI 均值: {ndvi.mean():.3f}')
print(src.profile)

src.close()
print('\n27 完成。下一题：28 出图看四个波段长什么样。')


# ---------- 自己动手 ----------
# 1. 把宣城-01 (118.76, 30.94) 也对到像元，看它落在哪、4 波段值多少。
#    两个站落在同一种地物上吗？（提示：一个在城市区，一个在植被区）
# 2. src.read(window=Window(col_off, row_off, width, height)) 能只读一小块，
#    试着只读 NDVI 最高那块区域，算它的均值。
# 3. src.profile 能拿到完整写入参数。想复制一个一模一样的 tif 时有用——
#    print(src.profile) 看看里面有什么。