"""28_raster_viz.py — 栅格出图：4 波段、真彩色合成、NDVI 热力图

三个核心知识点：
1. imshow 默认 row=0 在顶部 → 和栅格存储顺序一致 → 地理方向（北在上）正确
2. 真彩色合成 = 把 R/G/B 三个波段堆成 (H, W, 3) 的 RGB 图
3. extent 参数让坐标轴显示经纬度，而不是行/列号
"""
import numpy as np
import rasterio
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

src = rasterio.open('week04-rasterio/sample.tif')
arr = src.read()                              # (4, 40, 60) — (波段, 行, 列)

# 经纬度范围，给 imshow 的 extent 用
left, bottom, right, top = src.bounds          # (116.5, 30.5, 119.5, 32.5)

# ---------- 1. 四波段灰度图并排 ----------
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
titles = ['Blue 蓝光', 'Green 绿光', 'Red 红光', 'NIR 近红外']
for i, ax in enumerate(axes.flat):
    im = ax.imshow(arr[i], cmap='gray', extent=(left, right, bottom, top))
    ax.set_title(titles[i])
    ax.set_xlabel('经度')
    ax.set_ylabel('纬度')
    fig.colorbar(im, ax=ax, shrink=0.6, label='反射率')
fig.suptitle('sample.tif 四波段灰度图', fontsize=14)
fig.tight_layout()
fig.savefig('week04-rasterio/bands_gray.png', dpi=150)
print('图1已存: bands_gray.png')

# ---------- 2. 真彩色合成（R/G/B 三波段堆成 RGB）----------
# arr 顺序是 [B, G, R, NIR]，所以 R=arr[2], G=arr[1], B=arr[0]
rgb = np.stack([arr[2], arr[1], arr[0]], axis=-1)    # (40, 60, 3)
# 反射率范围 0-0.5，imshow 要 0-1，简单拉伸到 [0,1]
rgb_norm = rgb / 0.5
rgb_norm = np.clip(rgb_norm, 0, 1)

fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(rgb_norm, extent=(left, right, bottom, top))
ax.set_title('真彩色合成 (R/G/B)')
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
fig.tight_layout()
fig.savefig('week04-rasterio/rgb_composite.png', dpi=150)
print('图2已存: rgb_composite.png')

# ---------- 3. NDVI 栅格热力图 ----------
red, nir = arr[2], arr[3]
ndvi = (nir - red) / (nir + red)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1,
               extent=(left, right, bottom, top))
fig.colorbar(im, ax=ax, label='NDVI')
ax.set_title('NDVI 栅格（宣城-合肥区域）')
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
fig.tight_layout()
fig.savefig('week04-rasterio/ndvi_raster.png', dpi=150)
print('图3已存: ndvi_raster.png')

src.close()
print('\n28 完成。打开三张图核对：')
print('  bands_gray.png    — 看 NIR 波段，植被区应该最亮（反射率高）')
print('  rgb_composite.png — 植被偏绿、水体偏深蓝、城市偏灰白')
print('  ndvi_raster.png   — 植被深绿、水体深红、城市/裸土浅黄')


# ---------- 自己动手 ----------
# 1. 把 extent 去掉重跑一张 NDVI 图，坐标轴会变成行/列号。
#    对比两张图，理解"栅格的行列号"和"地理坐标"是同一块数据的两种坐标轴标注。
# 2. NIR 波段单独画一张彩色图（cmap='viridis'），和灰度图对比，
#    看彩色图是不是更容易区分水体（NIR 极低 → 深紫）和植被（NIR 高 → 黄）。
# 3. 用 src.read(window=rasterio.windows.Window(20, 15, 20, 15)) 只读中部一块，
#    算它的 NDVI 均值，看和整景均值 0.276 差多少——窗口读取是处理大影像不爆内存的关键。
