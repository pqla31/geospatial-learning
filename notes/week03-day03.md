# Week 3 Day 3 —— 空间查询：intersects / within / contains + sjoin

## 今天学什么

GIS 里一半的问题都是"谁和谁有空间关系"：

- 这个监测站落在哪个行政区里？
- 这条高速公路穿过哪些县？
- 这个保护区包含哪些村落？

答案全靠三个空间谓词 + 一个空间连接。

## 三个谓词（宽松 → 严格）

| 谓词 | 含义 | A↔B 关系 |
|---|---|---|
| `intersects` | A 和 B 有任何接触（哪怕只碰一条边） | 最宽松 |
| `within` | A 完全在 B 内部 | A 在 B 里 |
| `contains` | B 完全在 A 内部（= within 反向） | A 装着 B |

**关键点**：`A.within(B)` 和 `B.contains(A)` 是同一件事的两种说法，永远同时为真或同时为假。

**点的特殊性**：点没有面积、没有内部，所以 `point.within(polygon)` 和 `polygon.contains(point)` 严格等价——不像线和面那样有边界细节差异。今天都用点测试，简化判断。

## 空间连接 sjoin

普通 `pd.merge` 是按"列值相等"连表；`sjoin` 是按"几何关系"连表。

```python
gpd.sjoin(points, polygons, how='left', predicate='within')
#          ↑左表        ↑右表
```

- `predicate='within'`：左表的点是否落在右表的多边形内
- `how='left'`：保留左表所有点，落不进任何区的填 NaN（漏网点）
- `how='inner'`：只保留匹配上的（丢掉落不进任何区的点）

输出列：左表原列 + 右表原列（右表列名**自动加 `_right` 后缀**避免冲突），geometry 保留左表的。

## 今天两个文件

### `23_spatial_predicates.py`

建一个点（合肥-01）和两个区多边形，把三种谓词各 print 一遍，看清它们的真假差异。再建一个边界正好经过该点的多边形，演示 **intersects=True 但 within=False**——这是谓词"宽松→严格"的最直观证据。

### `24_sjoin.py`

读 `stations.csv` → GeoDataFrame（复用 Day 1），建两个行政区，用 `sjoin` 给每个站点打上它所属的区名，再出图。

## 验收标准

1. 能说清 `intersects` / `within` / `contains` 三者的区别，特别是为什么"边界接触"算 intersects 不算 within
2. 能说清 `A.within(B)` 和 `B.contains(A)` 为什么永远同时真或同时假
3. `sjoin` 输出里每个站点对应的区名正确：宣城两站 → 宣城区，合肥-01 → 合肥区
4. 能解释 `how='left'` 和 `how='inner'` 在"有点落不进任何区"时的输出差异

## 自己动手

- 改 `predicate='intersects'` 重跑 sjoin，看结果和 `within` 有没有区别（提示：点完全不接触多边形边界的，intersects 和 within 结果一样；只有点恰好落在边上才不同）
- 把某个区多边形画小一点，让一个站点落不进去，看 `how='left'` 那行是不是变成 NaN
- 用 `gdf_right[gdf_right.contains(point)]` 这种布尔筛选替代 sjoin，写法更接近 pandas 的味道，对比两种写法
