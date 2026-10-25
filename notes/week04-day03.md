# Week 4 Day 3 — 矢栅联动：用矢量裁栅格、把像元值提取到站点

## 今天学什么

矢栅联动 = 矢量（geopandas）和栅格（rasterio）真正叠到一起。两个核心操作：

1. **mask**：用矢量几何裁栅格，按区统计（分区统计 / zonal stats）
2. **点位提取**：把站点坐标对到像元，提取像元值（矢栅采样）

这是学期项目的核心一块 —— "每个行政区 NDVI 均值" 和 "每个站点的卫星观测" 都靠它。

## 矢栅联动铁律

**矢量和栅格 CRS 必须一致才能 mask。** Week 3 的 districts.shp 是 4326，sample.tif 也是 4326，正好对上。不一致的话先 `to_crs` 统一。

## 三个核心概念

**1. mask(src, [geometry], crop=True, nodata=...)**
- 输入：栅格 + 矢量几何列表
- 输出：(裁剪后数组, 新 transform)
- crop=True：裁到区的边界框，区外设 nodata
- nodata 像元必须排除后才能算统计

**2. src.index(lon, lat) → (row, col)**
- 经纬度找像元号（Day 1 学过，今天用在 12 行站点上）
- `src.read()[:, row, col]` 提取该像元所有波段值

**3. 点位观测 vs 像元观测（尺度效应）**
- 站点观测（地面实测）：测的是脚下 1 平方米，有时间序列
- 像元观测（卫星）：一个像元 5.6 km × 5.6 km，单时相
- 两者必然有差异，不是 bug —— 这就是遥感尺度效应

## 今天的文件

### 31_mask_raster.py — 用行政区裁栅格 + 分区统计
- CRS 一致性检查（矢量 4326 == 栅格 4326）
- 对每个区 mask sample.tif → 算 NDVI 均值
- 排除 nodata 像元（区外被设成 -9999 的不能算）
- 输出分区统计表

### 32_point_extract.py — 站点像元提取 + 尺度对比
- 12 行站点表对到栅格像元
- 每站提取 4 波段值 → 算卫星 NDVI
- 对比 csv 的 ndvi（站点月际观测）vs raster_ndvi（卫星单时相）
- 按站分组看 NIR 判断地物类型

## 验收标准

- [ ] 31 输出：CRS 一致性检查通过
- [ ] 31 输出：合肥区 NDVI ≈ -0.001（含城市+水体正负抵消）、宣城区 ≈ 0.546（含植被）
- [ ] 31 输出：两区各 600 有效像元（nodata 排除正确）
- [ ] 32 输出：同一站 4 个月 raster_ndvi 完全一样（卫星单时相）
- [ ] 32 输出：合肥-01 NIR ≈ 0.23（城市像元）、宣城 NIR ≈ 0.45（植被像元）
- [ ] 32 输出：能说清 csv ndvi 和 raster_ndvi 为什么不能直接比

## 三个坑

1. **nodata 必须排除**。mask 的 crop=True 会把区外像元设成 -9999，
   算均值前必须 `ndvi[ndvi != -9999]` 过滤，否则 -9999 会把均值拉到负无穷。
2. **CSV 的 ndvi 和栅格 NDVI 不能直接比**。csv 是月际时间序列（0.12-0.75），
   栅格是单时相空间观测（-1 到 0.8）。两者不是同时相、不是同传感器，
   差异体现尺度效应，不是"谁对谁错"。
3. **GDAL_DATA 警告**会弹几次，无害，脚本里用 warnings.filterwarnings 屏蔽了。

## 怎么跑

```bash
cd /e/Dota/projects/geospatial-learning
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/31_mask_raster.py
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/32_point_extract.py
git add .
git commit -m "feat: week04 day3 练习（矢栅联动：mask 裁栅格 + 站点像元提取）"
git push
```

## 为什么这节重要

- **分区统计**是遥感应用最常用的分析：每个行政区 NDVI 均值、每个流域 DEM 均值、
  每个地块作物长势 —— 本质都是"矢量分组 × 栅格统计"。
- **点位提取**是"地面观测 vs 卫星观测"验证的基础：
  要么拿站点验证卫星产品准不准，要么拿卫星补站点没覆盖的区域。
  Day 1 的 src.index 是单点操作，今天把它用在真实 12 行站点表上 —— 这是矢栅联动的实战。
