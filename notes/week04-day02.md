# Week 4 Day 2 — 栅格重投影 + 窗口读取

## 今天学什么

两个核心技能：

1. **重投影**：栅格从 4326（度）转到 3857（米），像元网格要重新切分
2. **窗口读取**：大影像只读一小块，不爆内存

## 栅格重投影 vs 矢量重投影

Week 3 矢量 `to_crs` 只换坐标，几何不变；栅格重投影是**把像元重新铺到新坐标系的网格上**——像元数会变、像元值会变（插值产生新值）。

| | 矢量 to_crs | 栅格 reproject |
|---|---|---|
| 改变 | 坐标 | 像元网格 + 像元值 |
| 像元数 | —（没像元） | 变（4326 的 40×60 → 3857 的 44×57） |
| 值变化 | 不变 | 插值产生新值（bilinear） |
| 原因 | 几何对象可平移 | 像元是规则网格，新网格和旧网格不对齐 |

## 三个核心概念

**1. calculate_default_transform — 算目标网格**
```python
dst_transform, dst_width, dst_height = calculate_default_transform(
    src.crs, dst_crs, src.width, src.height, *src.bounds
)
```
自动按目标 CRS 切分像元网格，返回新 transform 和尺寸。

**2. Resampling — 重采样方法**
- `bilinear`（双线性）：连续值数据用，反射率/DEM/温度。插值产生新值，极值会略缩。
- `nearest`（最近邻）：分类数据用，土地覆盖/类型图。不产生新类别。
- 选错会出问题：分类图用 bilinear 会产生不存在的混合类别。

**3. Window — 窗口读取**
```python
Window(col_off, row_off, width, height)  # 按像元号
```
经纬度→像元号手动换算（transform 公式反过来用）：
```python
col = (lon - transform.c) / transform.a
row = (lat - transform.f) / transform.e    # e 是负数
```

## 今天的文件

### 29_reproject.py — 4326 → 3857
- `calculate_default_transform` 算目标网格
- 4 波段 bilinear 重投影
- 对比源/目标的 transform/bounds/shape/NDVI
- 写成 `sample_3857.tif`

### 30_window_read.py — 窗口读取
- 全读 vs 窗口读的内存对比（9600 vs 800 个值）
- 按像元号开窗读水体区
- 经纬度→像元号换算开窗读植被区
- 站点 3×3 邻域采样
- 窗口裁剪存成 `water_clip.tif`

## 验收标准

- [ ] 29 输出：目标像元尺寸 ≈ 5879 米（5.9 km，和源 0.05 度在 31°N 量级吻合）
- [ ] 29 输出：像元数 2400 → 2508（变了，因为重新切网格）
- [ ] 29 输出：NDVI 极值略缩（-1.0 → -0.902），均值几乎不变（bilinear 插值的特性）
- [ ] 29 生成 `sample_3857.tif`，crs=3857，bounds 是大数字（米单位）
- [ ] 30 输出：水体窗口 NDVI 负值、植被窗口 NDVI 正值
- [ ] 30 输出：3×3 邻域 NIR 值打印出来，看站点周围地物均不均匀
- [ ] 30 生成 `water_clip.tif`（3 KB 小块）

## 三个坑

1. **`sample_3857.tif` 和 `water_clip.tif` 不入 git**（.gitignore 排除 *.tif）。
   跑 29/30 自动生成，和 sample.tif 同理。
2. **bilinear 让极值缩**：-1.0 可能变成 -0.902。这是插值特性不是 bug。
   如果要求值完全不变（如分类图），用 nearest。
3. **窗口范围 ≠ 纯地物区**：经纬度开窗读"植被区"，窗口可能含城市边缘，
   均值会被拉低。窗口是按坐标切的，不按地物切——要纯地物统计得用掩膜（Day 3）。

## 怎么跑

```bash
cd /e/Dota/projects/geospatial-learning
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/29_reproject.py
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/30_window_read.py
git add .
git commit -m "feat: week04 day2 练习（栅格重投影与窗口读取）"
git push
```

## 为什么这节重要

- **重投影**是 Day 3 矢栅联动的前置——矢量和栅格必须在同一坐标系才能叠。
  Week 3 的站点是 4326，下周用 shapefile 裁栅格时，要么矢量转 3857，要么栅格转 4326。
- **窗口读取**是处理真实遥感数据（Sentinel-2 单景 1.5 GB）的唯一可行方式。
  全读进内存的代码在真实数据上会直接 OOM 崩溃。
