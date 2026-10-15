# Week 3 · Day 2 —— 几何操作：buffer / area / distance + 重投影

昨天把表格变成了空间点。今天让这些点"动"起来：画缓冲区、量距离、算面积。

但动手前要先打通一个 GIS 最核心的概念：**坐标系分两类**。

- **地理坐标系（geographic CRS）**：经纬度。`EPSG:4326` 就是 GPS 用的 WGS84。
  单位是"度"。度不是米——1 度在赤道约 111 公里，在两极是 0。
- **投影坐标系（projected CRS）**：把地球铺平到平面上的坐标系，单位是米/公里。
  `EPSG:3857`（Web Mercator）就是高德/百度地图底层用的，单位是米。

**铁律：做 buffer / 算面积 / 量距离，必须先投影到米坐标系。**
在 4326 里 `buffer(0.01)` 出来的"圆"，单位是无意义的平方度，面积算出来没法解释。
重投影后 `buffer(10000)` 就是实打实的 10000 米。

一句话记住：**度用来定位，米用来量算。**

复用昨天的三座城市：合肥、宣城、芜湖。时间预算 1.5 小时。

---

## 21_geom_ops.py —— buffer / area / distance（约 40 分钟）

要求：

```python
import geopandas as gpd
from shapely.geometry import Point

# ---------- 1. 三座城市（Day 1 的数据）----------
cities = gpd.GeoDataFrame({
    'name': ['合肥', '宣城', '芜湖'],
    'geometry': [
        Point(117.23, 31.82),
        Point(118.76, 30.94),
        Point(118.38, 31.33),
    ],
}, crs='EPSG:4326')

# ---------- 2. 重投影：度 -> 米 ----------
cities_m = cities.to_crs('EPSG:3857')     # Web Mercator，单位米

# ---------- 3. buffer：画 10 公里缓冲区 ----------
buf = cities_m.geometry.buffer(10000)     # 10 公里
print(buf.area / 1e6)                     # 单位 km²，应接近 π·10² ≈ 314

# ---------- 4. distance：城市间距离 ----------
d = cities_m.geometry[0].distance(cities_m.geometry[1])
print(d / 1000, 'km')                      # 合肥 -> 宣城

# ---------- 5. 对比：在 4326 里 buffer 没意义 ----------
print(cities.geometry.buffer(0.01).area)  # "平方度"，无法解释
```

要点自查：
- `to_crs('EPSG:3857')` 是重投影。投影后 POINT 的坐标变成 1300 万、374 万这种大数，
  因为是以本初子午线/赤道为原点的米数。这是正常的，不是错。
- buffer 面积应该接近 π × 10² ≈ 314.16 km²。差一点点是因为 Web Mercator 在 30°N
  有轻微放大。要更精确可以用 UTM 投影（如 `EPSG:32651`）。
- **铁律再强调一遍**：在 4326 里别做 buffer/area/distance。看到坐标是小数（经纬度）
  就要警觉"这是度，不能直接量算"。

---

## 22_lines_polygons.py —— 线与面的几何操作（约 50 分钟）

要求：

```python
import geopandas as gpd
from shapely.geometry import LineString, Polygon
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 1. 造一条"高速"连三城 ----------
highway = LineString([(117.23, 31.82), (118.38, 31.33), (118.76, 30.94)])

# ---------- 2. 造一个研究区矩形 ----------
study_area = Polygon([(117.0, 30.7), (119.0, 30.7), (119.0, 32.0), (117.0, 32.0)])

# ---------- 3. 重投影后做正经操作 ----------
gdf_line = gpd.GeoDataFrame({'name': ['高速'], 'geometry': [highway]}, crs='EPSG:4326')
gdf_area = gpd.GeoDataFrame({'name': ['研究区'], 'geometry': [study_area]}, crs='EPSG:4326')
gdf_line_m = gdf_line.to_crs('EPSG:3857')
gdf_area_m = gdf_area.to_crs('EPSG:3857')

# ---------- 4. buffer：高速两侧 5 公里走廊 ----------
corridor = gdf_line_m.geometry.buffer(5000)

# ---------- 5. 画出来 ----------
fig, ax = plt.subplots(figsize=(8, 6))
gdf_area_m.boundary.plot(ax=ax, color='gray', linewidth=1, label='研究区')
corridor.plot(ax=ax, color='orange', alpha=0.5, label='5km 走廊')
gdf_line_m.plot(ax=ax, color='red', linewidth=2, label='高速公路')
ax.set_title('高速公路 5 公里走廊与研究区')
ax.legend()
fig.savefig('week03-geopandas/highway_corridor.png', dpi=150)
```

要点自查：
- `LineString` 用一串坐标点造线，`Polygon` 用一串坐标点造面（首尾自动闭合）。
- `boundary.plot()` 画的是多边形的外框线，不是填色——用来叠图时避免遮挡别的图层。
- X/Y 轴显示 1300 万、370 万这种大数是 Web Mercator 的正常表现（米坐标从本初
  子午线/赤道算起），不是 bug。习惯了之后看到这个量级就知道是 3857。

---

## 验收标准（三条全中才算过）

1. 能说出地理坐标系（4326，度）和投影坐标系（3857，米）的区别，以及"做 buffer
   前必须 to_crs"的原因
2. buffer 10km 的面积输出接近 314 km²（π×10²），能解释为什么是这个数
3. `highway_corridor.png` 上三层叠图清晰：灰色研究区外框 + 橙色走廊 + 红色高速线

---

## 收工命令

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week03 day2 练习（几何操作与重投影）"
git push
```
