# geospatial-learning

合肥工业大学（宣城校区）地球信息科学与技术专业，2025 级。
从 2026-09（大二上）开始，记录 GIS 开发方向的练手过程：Python 基础 → 地学数据处理 → WebGIS → 三维 → 遥感 AI。

## 环境

- Python 环境名：**`gis`**（Anaconda 独立环境，Python 3.9.23）
- 激活：`conda activate gis`
- 已装好的包：numpy 2.0.2 / pandas 2.3.1 / matplotlib 3.9.4 / **geopandas 1.0.1 / rasterio 1.4.3 / shapely 2.0.7**

常用命令备忘：

```bash
conda activate gis          # 进环境（每次开终端都要先敲这句）
python script.py            # 跑脚本
conda env list              # 看有哪些环境
```

## 目录

| 目录 | 放什么 |
|---|---|
| `week01-basics/` | Python 基础练习（大二上前 4 周） |
| `notes/` | 学习笔记和踩坑记录 |
| `data/` | 数据文件，**不入库**（已写进 .gitignore） |

## 节奏

每天 1.5 小时，不断档。断三天要花一天找回状态。——周末突击 8 小时不如每天 1.5 小时。

## 本学期的「不做」清单

Vue、Cesium、深度学习、Java、沉迷 ArcGIS 界面操作。
这学期只有三个目标：Python 能真处理地学数据、能手写静态页面、GitHub 有持续提交记录。
