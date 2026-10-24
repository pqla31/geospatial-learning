"""30_window_read.py — 窗口读取：只读影像的一小块

真实遥感影像动辄几个 GB，src.read() 全读进内存会爆。
窗口读取只拿需要的那块——这是处理大影像的必备技能。

两种开窗方式：
1. Window(col_off, row_off, width, height) — 按像元号
2. 手动经纬度→像元号换算 — 用 transform 公式反过来算
"""
import numpy as np
import rasterio
from rasterio.windows import Window

src = rasterio.open('week04-rasterio/sample.tif')

# ---------- 1. 全读 vs 窗口读：看内存差别 ----------
full = src.read()
print(f'=== 全读 ===')
print(f'  shape: {full.shape}, 字节: {full.nbytes / 1024:.1f} KB')
print('  → 真实影像 5000×5000×7 波段 float32 ≈ 700 MB，全读就吃内存')

# ---------- 2. 按像元号开窗：读水体区 ----------
# gen_sample_tif 里水体在 row 15-25, col 10-30
water_win = Window(col_off=10, row_off=15, width=20, height=10)
water = src.read(window=water_win)
print(f'\n=== 水体窗口（row 15-25, col 10-30）===')
print(f'  Window: {water_win}')
print(f'  shape: {water.shape}, 字节: {water.nbytes / 1024:.1f} KB')
print(f'  只读了 {water.size} 个值，vs 全读 {full.size} 个')

water_ndvi = (water[3] - water[2]) / (water[3] + water[2])
print(f'  水体区 NDVI: mean={water_ndvi.mean():.3f} (应为负)')

# ---------- 3. 按经纬度范围开窗：读植被区 ----------
# 宣城在 118.0-119.5E, 30.5-31.5N
# 经纬度 → 像元号换算（就是 transform 公式反过来用）：
#   col = (lon - c) / a       （c=左上经度, a=像元宽）
#   row = (lat - f) / e       （f=左上纬度, e=像元高负值）
left, bottom, right, top = 118.0, 30.5, 119.5, 31.5
col_off = int((left - src.transform.c) / src.transform.a)
row_off = int((top - src.transform.f) / src.transform.e)
win_w = int((right - left) / src.transform.a)
win_h = int((top - bottom) / src.transform.a)   # 纬度差转行数（a 和 -e 同值）
veg_win = Window(col_off, row_off, win_w, win_h)
veg = src.read(window=veg_win)
print(f'\n=== 植被窗口（118.0-119.5E, 30.5-31.5N）===')
print(f'  经纬度 → 像元: col_off={col_off}, row_off={row_off}, {win_w}×{win_h}')
print(f'  Window: {veg_win}')
print(f'  shape: {veg.shape}')
veg_ndvi = (veg[3] - veg[2]) / (veg[3] + veg[2])
print(f'  植被区 NDVI: mean={veg_ndvi.mean():.3f} (应为正值，但窗口含城市边缘会拉低)')

# ---------- 4. 站点周围 3×3 邻域采样 ----------
# 合肥-01 站点 → 像元号 → 开 3×3 窗
lon, lat = 117.23, 31.82
row, col = src.index(lon, lat)
hood = src.read(window=Window(col - 1, row - 1, 3, 3))   # 中心 ±1 像元
print(f'\n=== 合肥-01 周围 3×3 邻域 ===')
print(f'  中心像元: row={row}, col={col}')
print(f'  窗口 shape: {hood.shape}  (bands, 3, 3)')
print(f'  NIR 波段 3×3:')
print(hood[3])   # 第 4 波段（NIR）打印 3×3 矩阵
print(f'  → 9 个像元的 NIR 值，看站点周围地物均不均匀')

# ---------- 5. 窗口写回：复制一小块到新文件 ----------
# 实战场景：从大影像裁出一小块研究区单独存档
profile = src.profile.copy()
profile.update(width=20, height=10)
with rasterio.open('week04-rasterio/water_clip.tif', 'w', **profile) as f:
    f.write(water)
print(f'\n已裁出水体块到 water_clip.tif ({water.nbytes/1024:.1f} KB)')

src.close()
print('\n30 完成。')


# ---------- 自己动手 ----------
# 1. 用手动换算裁出宣城-01 (118.76, 30.94) 周围 0.2 度的块，存成 tif
#    （0.2 度 ≈ 22 km，足够覆盖一个小流域。算 col_off/row_off 时记得 ±0.1 居中）
# 2. 对比 water_clip.tif 和原 sample.tif 的 transform——
#    裁剪后 transform 的 .c/.f（左上角坐标）应该变了，但 .a/.e（像元尺寸）不变
# 3. 算一下：如果只关心水体区的 NDVI，全读再切片 vs 直接窗口读，
#    后者省了多少内存？（提示：2400 vs 200 个像元）
