"""生成教学用多波段遥感影像 sample.tif

覆盖宣城-合肥一带（116.5-119.5E, 30.5-32.5N），4 波段（B/G/R/NIR）。
空间模式按真实地物设计：
- 北部城市区：高反射率（白屋顶）
- 中部水体（模拟巢湖一带）：低反射率，NIR 极低 → NDVI 负
- 南部植被区（宣城林区）：Red 低 NIR 高 → NDVI 高正值
- 其余裸土：中等反射率

跑完会在同目录生成 sample.tif，供 27/28 读取练习。
"""
import numpy as np
import rasterio
from rasterio.transform import from_origin

np.random.seed(42)

# ---------- 网格定义 ----------
# 60 列 × 40 行，分辨率 0.05 度，覆盖 3°×2° 区域
width, height = 60, 40
lon_min, lat_max = 116.5, 32.5      # 左上角（transform 用左上）
res = 0.05                          # 每像元 0.05 度 ≈ 5.5 km
transform = from_origin(lon_min, lat_max, res, res)

col_grid, row_grid = np.meshgrid(np.arange(width), np.arange(height))  # (40, 60)

# ---------- 按地物造反射率 ----------
# 基础反射率：随纬度从北到南略升
base = 0.15 + 0.1 * (row_grid / height)

city_mask = (row_grid < 10) & (col_grid < 20)                         # 北部城市
water_mask = (row_grid >= 15) & (row_grid < 25) & (col_grid >= 10) & (col_grid < 30)  # 巢湖水体
veg_mask = row_grid >= 25                                            # 南部植被

blue = base.copy() * 1.0
green = base.copy() * 1.2
red = base.copy() * 1.1
nir = base.copy() * 1.3

# 城市屋顶：四波段都高
blue[city_mask] = 0.35; green[city_mask] = 0.38; red[city_mask] = 0.40; nir[city_mask] = 0.42
# 水体：可见光低，近红外极低（水吸收 NIR）
blue[water_mask] = 0.08; green[water_mask] = 0.06; red[water_mask] = 0.04; nir[water_mask] = 0.02
# 植被：红光低（叶绿素吸收），近红外高（叶肉散射）
blue[veg_mask] = 0.05; green[veg_mask] = 0.08; red[veg_mask] = 0.08; nir[veg_mask] = 0.45

# 加一点噪声，让它像真实影像
noise = lambda: np.random.normal(0, 0.01, (height, width))
blue = np.clip(blue + noise(), 0, 1).astype('float32')
green = np.clip(green + noise(), 0, 1).astype('float32')
red = np.clip(red + noise(), 0, 1).astype('float32')
nir = np.clip(nir + noise(), 0, 1).astype('float32')

data = np.stack([blue, green, red, nir], axis=0)  # (4, 40, 60) — (波段, 行, 列)

# ---------- 写 tif ----------
profile = {
    'driver': 'GTiff',
    'height': height,
    'width': width,
    'count': 4,
    'dtype': 'float32',
    'crs': 'EPSG:4326',
    'transform': transform,
    'nodata': -9999.0,
    'compress': 'lzw',
}

with rasterio.open('week04-rasterio/sample.tif', 'w', **profile) as dst:
    dst.write(data)
    dst.descriptions = ('Blue', 'Green', 'Red', 'NIR')
    dst.units = ('reflectance',) * 4

print('sample.tif 生成完成')
print(f'  波段数: {profile["count"]} (B/G/R/NIR)')
print(f'  尺寸: {width} x {height} 像元')
print(f'  覆盖: {lon_min}E - {lon_min+width*res}E, {lat_max-height*res}N - {lat_max}N')
print(f'  分辨率: {res} 度/像元 ≈ {res*111:.1f} km')

# 读回自检
with rasterio.open('week04-rasterio/sample.tif') as src:
    print(f'\n读回校验:')
    print(f'  CRS: {src.crs.to_epsg()}')
    print(f'  bounds: {tuple(round(b,3) for b in src.bounds)}')
    print(f'  bands: {src.count}, 描述: {src.descriptions}')
    print(f'  shape: (bands, height, width) = ({src.count}, {src.height}, {src.width})')
    arr = src.read()
    ndvi = (arr[3] - arr[2]) / (arr[3] + arr[2])
    print(f'  NDVI 范围: {ndvi.min():.3f} ~ {ndvi.max():.3f}')
    print(f'    水体区 NDVI 均值: {ndvi[15:25, 10:30].mean():.3f} (应为负)')
    print(f'    植被区 NDVI 均值: {ndvi[25:40, :].mean():.3f} (应为 0.7+)')
