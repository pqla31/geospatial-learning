# Week 3 Day 2 —— 线与面：LineString/Polygon 的几何操作
# 对应任务单：notes/week03-day02.md
import geopandas as gpd
from shapely.geometry import LineString, Polygon
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# ---------- 1. 造一条"高速"连三城 ----------
# 合肥(117.23, 31.82) -> 芜湖(118.38, 31.33) -> 宣城(118.76, 30.94)
highway = LineString([(117.23, 31.82), (118.38, 31.33), (118.76, 30.94)])
print('--- 高速公路（度坐标系下）长度:', highway.length, '度 ---')


# ---------- 2. 造一个研究区矩形 ----------
# 一个把三城圈住的矩形
study_area = Polygon([(117.0, 30.7), (119.0, 30.7), (119.0, 32.0), (117.0, 32.0)])
print('研究区面积:', study_area.area, '平方度')


# ---------- 3. 重投影后做正经操作 ----------
gdf_line = gpd.GeoDataFrame({'name': ['高速'], 'geometry': [highway]}, crs='EPSG:4326')
gdf_area = gpd.GeoDataFrame({'name': ['研究区'], 'geometry': [study_area]}, crs='EPSG:4326')
gdf_line_m = gdf_line.to_crs('EPSG:3857')
gdf_area_m = gdf_area.to_crs('EPSG:3857')

print('\n--- 重投影后（米）---')
print(f'高速公路长度: {gdf_line_m.geometry.iloc[0].length/1000:.1f} km')
print(f'研究区面积: {gdf_area_m.geometry.iloc[0].area/1e6:.0f} km²')


# ---------- 4. buffer：高速两侧 5 公里走廊 ----------
corridor = gdf_line_m.geometry.buffer(5000)
print(f'5km 走廊面积: {corridor.iloc[0].area/1e6:.1f} km²')


# ---------- 5. 画出来：三层叠图 ----------
fig, ax = plt.subplots(figsize=(8, 6))
gdf_area_m.boundary.plot(ax=ax, color='gray', linewidth=1, label='研究区')
corridor.plot(ax=ax, color='orange', alpha=0.5, label='5km 走廊')
gdf_line_m.plot(ax=ax, color='red', linewidth=2, label='高速公路')
ax.set_title('高速公路 5 公里走廊与研究区')
ax.set_xlabel('X (米, Web Mercator)')
ax.set_ylabel('Y (米)')
ax.legend()
fig.tight_layout()
fig.savefig('week03-geopandas/highway_corridor.png', dpi=150)
print('\n图已保存：week03-geopandas/highway_corridor.png')


# ---------- 自己动手 ----------
# 1. 把走廊宽度改成 10km，看面积是不是大约翻倍（线 buffer 面积 ≈ 长×宽）
# 2. corridor.iloc[0].intersection(gdf_area_m.geometry.iloc[0]) 算走廊与研究区相交面积
# 3. 加一个你家乡的 Point，用 point.within(study_area) 看它在不在这个矩形里
