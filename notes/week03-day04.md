# Week 3 Day 4 —— Shapefile 读写 + 综合出图（Week 3 收官）

## 今天目标

把前三天的技能串成一条完整流程：**读 shapefile → sjoin 聚合 → 重投影 → buffer → 分级填色出图**。这就是 GIS 工程里"点数据 → 空间聚合 → 面统计 → 可视化"的标准管线。

## 文件

| 文件 | 内容 |
|---|---|
| `25_shapefile_io.py` | shapefile 多文件结构、读写、中文编码坑 |
| `26_composite_map.py` | 综合出图：四层叠图，串起三天技能 |

## 25 核心知识点

### shapefile 是 5 件套，不是单文件

写一个 `districts.shp` 会生成 5 个文件：

| 后缀 | 作用 |
|---|---|
| `.shp` | 几何数据（坐标/顶点） |
| `.shx` | 空间索引（快速查找） |
| `.dbf` | 属性表（列数据） |
| `.prj` | 坐标系定义 |
| `.cpg` | 编码声明（UTF-8，中文才不乱） |

**拷给别人要打包整个文件夹**，少一个都打不开。

### 中文编码

geopandas 1.0+ 默认写 UTF-8 + `.cpg` 声明，中文读回正常。
老版本或纯 UTF-8 无 `.cpg` 会乱码 → `to_file(encoding='gbk')` + `read_file(encoding='gbk')`。

### 字段名 10 字节限制（最大的坑）

`.dbf` 字段名限 10 字节。中文 UTF-8 占 3 字节/字：

| 字段名 | 字节数 | 结果 |
|---|---|---|
| `区名` | 6 | OK |
| `站名` | 6 | OK |
| `行政区名` | 12 | **崩** |
| `观测站点名称` | 18 | **崩** |

→ 中文字段名最多 **3 个字**。想用长名？换 GeoJSON，没这限制。
→ 或者字段名用英文（`station`/`district`），值用中文没问题。

### GeoJSON vs Shapefile

| | GeoJSON | Shapefile |
|---|---|---|
| 文件数 | 1 个 | 5 个 |
| 格式 | 文本（能记事本打开） | 二进制 |
| 字段名限制 | 无 | 10 字节 |
| 中文 | 默认 UTF-8 无忧 | 要靠 .cpg |
| 适用场景 | Web、小数据、教学 | 传统 GIS 工程、大数据 |

两种 QGIS / ArcGIS 都能开。

## 26 综合出图流程

```
1. read_file 读 shapefile      ← 今天学的
2. sjoin 站点落区              ← Day 3
3. groupby 按区聚合 NDVI 均值   ← Day 2 + Day 3
4. merge 均值写回区表          ← pandas
5. to_crs 重投影到米           ← Day 2
6. buffer 5km 缓冲区           ← Day 2
7. plot column 分级填色出图     ← Day 1 + matplotlib
```

出图四层：
- 层 1：行政区按 NDVI 均值填色（`cmap='RdYlGn'`，合肥区偏黄 0.49、宣城区偏绿 0.58）
- 层 2：站点 5km buffer 半透明圆
- 层 3：站点红色实心点
- 层 4：站名 + 区名标注

## 验收标准

1. `25` 跑完，`shp/` 下有 10 个文件（districts + stations 各 5 件套）+ 1 个 geojson
2. 读回的中文正常（区名、站名不乱码）
3. `26` 跑完生成 `composite_map.png`，图上有：填色区 + 蓝圈 buffer + 红点站点 + 标注 + 图例
4. 能说清楚 shapefile 为什么是 5 个文件、字段名为什么限 10 字节

## 自己动手

### 25
1. 记事本打开 `districts.geojson`，看 JSON 结构
2. 把"站名"改成"观测站点名称"（6 字），跑看报什么错
3. 删 `.cpg` 再读，看中文会不会乱

### 26
1. buffer 改 10km，看宣城两站缓冲区是否重叠（两站相距约 5km）
2. 换 `cmap='YlGn'`（黄到绿，适合植被）
3. 加每区 NDVI 标准差标注

## Week 3 收官

做完今天，Week 3 四天全齐：

| Day | 主题 | 核心动作 |
|---|---|---|
| 1 | GeoDataFrame 入门 | `points_from_xy` / `crs` / `to_file` |
| 2 | 几何操作 | `buffer` / `area` / `distance` / `to_crs` |
| 3 | 空间查询 | `intersects` / `within` / `sjoin` |
| 4 | shapefile + 综合 | `read_file` / `to_file` / 四层出图 |

下周进 **rasterio**——读遥感影像（.tif），算 NDVI 栅格，把矢量和栅格联动。
