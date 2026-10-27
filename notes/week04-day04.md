# Week 4 Day 4 — 学期项目收口：NDVI 计算 + 分区统计完整流程

## 今天学什么

把 Week 1-4 学的全部串成一条完整流程，出两张综合图。这不是新知识点，
是"整合" —— 验证你真的能把 4 周的碎片技能拼成一个能跑的东西。

## 流程回顾（每步对应哪周学的）

```
读遥感影像 sample.tif          ← Week 4 Day 1 rasterio
    ↓
算 NDVI 栅格 (nir-red)/(nir+red) ← Week 1 NumPy 公式
    ↓
读行政区 districts.shp          ← Week 3 geopandas
    ↓
分区统计 NDVI 均值 (mask)       ← Week 4 Day 3 矢栅联动
    ↓
站点像元提取                    ← Week 4 Day 3 + Week 2 站点表
    ↓
出综合图                        ← Week 1 matplotlib + Week 3 叠图
```

## 今天的文件

### 33_pipeline.py — 完整流程，两张图

**pipeline_map.png** —— 主成果图：
- NDVI 栅格底图（RdYlGn，vmin=-1 vmax=1）
- 行政区黑色边界叠图
- 区名 + NDVI 均值标注（白底框）
- 三个站点彩色标注（合肥红、宣城两站蓝/橙）

**pipeline_stats.png** —— 统计对比：
- 左：分区 NDVI 均值柱状图（合肥区 vs 宣城区）
- 右：站点观测均值 vs 卫星像元 NDVI 并排柱状图

## 验收标准

- [ ] pipeline_map.png：NDVI 栅格 + 区边界 + 站点三层都在
- [ ] pipeline_map.png：区名标注含 NDVI 值（合肥区 -0.001、宣城区 0.546）
- [ ] pipeline_map.png：三站点颜色区分、站名标注不重叠
- [ ] pipeline_stats.png：左图合肥区红柱（负/低）、宣城区绿柱（高）
- [ ] pipeline_stats.png：右图站点观测 vs 卫星像元并排，能看出尺度差异
- [ ] 脚本能一口气跑完不报错（6 步流程全通）

## 怎么跑

```bash
cd /e/Dota/projects/geospatial-learning
D:/hhh/apps/anaconda/envs/gis/python.exe week04-rasterio/33_pipeline.py
git add .
git commit -m "feat: week04 day4 学期项目收口（NDVI 分区统计完整流程）"
git push
```

PNG 本机生成（沙箱杀 matplotlib savefig，老规矩）。

## Week 4 四天回顾

| Day | 主题 | 核心 |
|---|---|---|
| 1 | rasterio 入门 | `open` / `read` / `transform` / `index` / `imshow` |
| 2 | 重投影 + 窗口 | `reproject` / `Resampling` / `Window` |
| 3 | 矢栅联动 | `mask` 裁栅格 / 站点像元提取 |
| 4 | 项目收口 | 6 步流程串通 + 综合出图 |

## 学期阶段一收官（Python 基础 第 1-5 周）

到这里，你这学期阶段一的三个目标全部达成：

1. **Python 地学** —— 能读遥感影像、算 NDVI、分区统计、出综合图
2. **GitHub** —— 从零到 33 个练习脚本 + 15 张成果图，绿点持续在亮
3. 前端 HTML/CSS —— 下周开始

仓库里现在有：
- `week01-basics/` — Python 基础 + NumPy + matplotlib（10 个脚本）
- `week02-pandas/` — pandas 表格处理（8 个脚本 + CSV）
- `week03-geopandas/` — 矢量数据全套（8 个脚本 + shapefile + geojson）
- `week04-rasterio/` — 栅格遥感影像（7 个脚本 + 综合图）

从 9 月 22 日连 `git add` 都没听过，到现在能独立跑通"读影像→算 NDVI→分区统计→出图"的完整流程。5 周，零基础到能做学期项目。
