# Week 4 Day 1 — rasterio 入门：读 .tif、认识栅格数据结构

## 今天学什么

**栅格 = 像元的矩阵 + 地理坐标信息。** 和前 3 周学的"表"（pandas/geopandas）是两类完全不同的空间数据：

| | 矢量（geopandas） | 栅格（rasterio） |
|---|---|---|
| 数据结构 | 点/线/面 + 属性表 | 像元矩阵 + transform |
| 单位 | 几何对象 | 规则网格的值 |
| 典型来源 | 行政边界、道路、地块 | 遥感影像、DEM、土地覆盖图 |
| 文件格式 | .shp / .geojson | .tif（GeoTIFF） |

NumPy 数组也能存矩阵，但 NumPy **不知道每个数字对应地面哪里**。rasterio 在 NumPy 数组上加了 `transform`（像元号↔坐标换算表）和 `crs`（坐标系），这才是空间数据。今天就是打通这一层。

## 三个核心概念

**1. transform —— 像元号和地理坐标的换算表**
```
x = a * col + c      （经度 = 像元宽 × 列号 + 左上角经度）
y = e * row + f      （纬度 = -像元高 × 行号 + 左上角纬度）
```
栅格存的时候 row 0 在最上面（纬度大），所以 `e` 是负数。

**2. read() 返回 (波段, 行, 列) 三维数组**
- `src.read()` → 全部波段 `(4, 40, 60)`
- `src.read(1)` → 第 1 波段 `(40, 60)`（2D）
- `src.read()[:, row, col]` → 某个像元的所有波段值

**3. index() 和 xy() —— 坐标↔像元互转**
- `src.index(lon, lat)` → `(row, col)`  经纬度找像元
- `src.xy(row, col)` → `(lon, lat)`  像元找中心坐标

这是矢栅联动的核心——"站点落在哪个像元、像元值多少"就靠它。

## 今天的文件

### gen_sample_tif.py — 先跑这个生成数据
造一个 4 波段（B/G/R/NIR）的教学影像，60×40 像元，覆盖宣城-合肥区域。
空间模式按真实地物设计：北部城市、中部水体（模拟巢湖）、南部植被。
跑完在 `week04-rasterio/` 生成 `sample.tif`。

### 27_rasterio_intro.py — 读 tif、认元数据
- 元数据：`count` / `width` / `height` / `dtypes` / `crs` / `transform` / `bounds` / `nodata` / `descriptions`
- transform 四属性：`.a`（像元宽）、`.e`（像元高负值）、`.c`（左上经度）、`.f`（左上纬度）
- 逐波段统计：`src.read(i)` 单波段 → 2D 数组
- 站点采样：把合肥-01 坐标对到像元，读 4 波段值
- 算 NDVI 栅格：复用 Week 1 公式 `(nir-red)/(nir+red)`，但这次在真实栅格上

### 28_raster_viz.py — 三张图
1. **bands_gray.png** — 4 波段灰度图并排，带经纬度坐标轴
2. **rgb_composite.png** — 真彩色合成（R/G/B 三波段堆 RGB）
3. **ndvi_raster.png** — NDVI 热力图，RdYlGn, vmin=-1 vmax=1

## 验收标准

- [ ] 跑完 gen_sample_tif.py，`sample.tif` 存在
- [ ] 27 输出：CRS=4326、bounds=(116.5, 30.5, 119.5, 32.5)、NDVI 范围含负值
- [ ] 27 输出：合肥-01 落在 row=13, col=14，像元中心坐标和站点坐标差 < 0.01 度
- [ ] 28 出图：NIR 波段植被区最亮、水体区最暗（NIR 是区分植被/水体的最佳波段）
- [ ] 28 出图：NDVI 图南方深绿、中部深红、能说清为什么

## 两个坑

1. **`.tif` 不入 git**（`.gitignore` 排除了 `*.tif`）。所以 `sample.tif` 不会上传 GitHub——
   `gen_sample_tif.py` 入仓，别人 clone 后跑一次自己生成。和 Week 3 的 shapefile 同理。
2. **`GDAL_DATA is not defined` 警告**：打开/写 tif 时会弹一条，无害，不用管。
   是 conda 环境变量没设全，不影响读写。

## 怎么跑

```bash
cd /e/Dota/projects/geospatial-learning
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/gen_sample_tif.py
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/27_rasterio_intro.py
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/28_raster_viz.py
git add .
git commit -m "feat: week04 day1 练习（rasterio 读 tif 与栅格出图）"
git push
```
