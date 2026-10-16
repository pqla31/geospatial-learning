# Week 3 Day 3 —— 空间谓词：intersects / within / contains
# 对应任务单：notes/week03-day03.md
import geopandas as gpd
from shapely.geometry import Point, Polygon

# ---------- 1. 一个点 + 两个区 ----------
# 合肥-01 站点（复用 stations.csv 里的坐标）
point = Point(117.23, 31.82)

# 两个行政区多边形：边界是 118.0 经线
# 合肥在西（117.23 < 118.0），落进"合肥区"
hefei_qu = Polygon([(116.5, 31.5), (118.0, 31.5),
                    (118.0, 32.5), (116.5, 32.5)])
# 宣城在东（118.76 > 118.0），落进"宣城区"
xuancheng_qu = Polygon([(118.0, 30.5), (119.5, 30.5),
                        (119.5, 31.5), (118.0, 31.5)])

print('=== 1. 三个谓词各 print 一遍 ===')
print(f'合肥-01 点坐标: {point}')
print(f'合肥区边界: {hefei_qu.bounds}')   # (minx, miny, maxx, maxy)
print(f'宣城区边界: {xuancheng_qu.bounds}')
print()

# intersects: 任何接触都算 True（最宽松）
print('--- intersects（碰着就行）---')
print(f'点 ∩ 合肥区: {point.intersects(hefei_qu)}')     # True
print(f'点 ∩ 宣城区: {point.intersects(xuancheng_qu)}')  # False
print()

# within: 点必须完全在多边形内部（不含边界）
print('--- within（点在区里）---')
print(f'点 ⊂ 合肥区: {point.within(hefei_qu)}')         # True
print(f'点 ⊂ 宣城区: {point.within(xuancheng_qu)}')      # False
print()

# contains: 反向——区是否完全包含点
print('--- contains（区装着点，是 within 的反向）---')
print(f'合肥区 ⊃ 点: {hefei_qu.contains(point)}')        # True
print(f'宣城区 ⊃ 点: {xuancheng_qu.contains(point)}')   # False
print()


# ---------- 2. 边界场景：intersects=True 但 within=False ----------
# 建一个多边形，它的一条边正好经过 (117.23, 31.82)
# 把合肥-01 点放在这个多边形的边界上
edge_poly = Polygon([(117.23, 31.0), (118.0, 31.0),
                     (118.0, 32.0), (117.23, 32.0)])
# 这条边 x=117.23 从 y=31 到 y=32，正好穿过点 (117.23, 31.82)

print('=== 2. 边界场景：点正好落在边上 ===')
print(f'多边形西边界 x=117.23，点 x=117.23 → 点在边上')
print(f'intersects: {point.intersects(edge_poly)}')   # True（碰着边）
print(f'within:     {point.within(edge_poly)}')       # False（不在内部）
print(f'contains:   {edge_poly.contains(point)}')     # False
print()
print('→ 这就是 intersects 比 within 宽松的实例')
print('  intersects 算"碰着"，within 要求"在内部"，边界不算内部')
print()


# ---------- 3. 等价关系：A.within(B) ⟺ B.contains(A) ----------
print('=== 3. within 和 contains 互为反向 ===')
print(f'点.within(合肥区):    {point.within(hefei_qu)}')
print(f'合肥区.contains(点):  {hefei_qu.contains(point)}')
print('→ 两者永远同时真或同时假，是同一件事的两种说法')
print()


# ---------- 4. 面对面的谓词：两个区是否相邻 ----------
print('=== 4. 两个区是否相邻（共享边界）===')
print(f'合肥区.intersects(宣城区): {hefei_qu.intersects(xuancheng_qu)}')  # True
print(f'合肥区.within(宣城区):     {hefei_qu.within(xuancheng_qu)}')      # False
print(f'合肥区.touches(宣城区):    {hefei_qu.touches(xuancheng_qu)}')     # True
print()
print('→ 相邻的两个区 intersects=True、within=False')
print('  touches 是 intersects 的特例：只碰边、不重叠面积')


# ---------- 自己动手 ----------
# 1. 把宣城区改成 Polygon([(117.5, 30.5), (119.5, 30.5), (119.5, 31.5), (117.5, 31.5)])
#    再算宣城-01 (118.76, 30.94) 是否还在区内，边界是否变了
# 2. 用 Point(118.0, 31.0)（边界交点）测三个谓词，看 intersects/within/contains 的真假
# 3. 算合肥区与宣城区的 intersection（相交部分），看是线还是面
