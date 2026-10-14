# Week 3 Day 1 —— GeoDataFrame：pandas 表格 + 几何列
# 对应任务单：notes/week03-day01.md
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

# ---------- 1. 从零造一个 GeoDataFrame ----------
# 和上周造 DataFrame 只差一点：多传一个 geometry 列
# geometry 单元格里存的是 Shapely 几何对象，不是数字
cities = gpd.GeoDataFrame({
    'name': ['合肥', '宣城', '芜湖'],
    'pop': [963, 250, 380],
    'geometry': [
        Point(117.23, 31.82),       # Point(经度, 纬度) —— x 在前！
        Point(118.76, 30.94),
        Point(118.38, 31.33),
    ],
})
print('--- cities ---')
print(cities)
print('\n类型:', type(cities).__name__)
print('\n--- cities.dtypes（注意 geometry 列的类型）---')
print(cities.dtypes)


# ---------- 2. GeoSeries：geometry 列本身 ----------
print('\n--- cities.geometry ---')
print(cities.geometry)
print('\n所有点的经度 .x:', cities.geometry.x.tolist())
print('所有点的纬度 .y:', cities.geometry.y.tolist())


# ---------- 3. pandas 操作全部照用 ----------
# 上周学的在 GeoDataFrame 上原样能跑——这就是"只多一列"的含义
print('\n--- 布尔筛选：pop > 300 ---')
print(cities[cities['pop'] > 300])
print('\npop 均值:', cities['pop'].mean())


# ---------- 4. 几何对象自带属性 ----------
# 注意：还没指定坐标系，单位是"度"，数字只用来理解概念
line = LineString([(117, 31), (118, 31), (118, 32)])
poly = Polygon([(117, 31), (118, 31), (118, 32)])
print('\n线长（度）:', line.length)
print('面积（平方度）:', poly.area)
print('质心:', poly.centroid)


# ---------- 5. total_bounds：数据覆盖范围 ----------
# [最小经度, 最小纬度, 最大经度, 最大纬度]
print('\ntotal_bounds:', cities.total_bounds)


# ---------- 自己动手 ----------
# 1. 给 cities 加一行你家乡的城市（先查它的经纬度，注意经度在前）
# 2. cities.geometry.distance(Point(120.0, 30.0)) 算各点到杭州的距离（单位还是度）
# 3. 用上周的 groupby 思路试试：cities.groupby 后按 x 坐标排序（提示 sort_values 用 cities.geometry.x）
