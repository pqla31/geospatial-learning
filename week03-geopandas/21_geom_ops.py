# Week 3 Day 2 —— 几何操作：buffer / area / distance + 重投影
# 对应任务单：notes/week03-day02.md
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
print('--- 原始（经纬度，单位是度）---')
print(cities)


# ---------- 2. 重投影：度 -> 米 ----------
# EPSG:3857 = Web Mercator（投影坐标系，单位米）
# 不重投影就 buffer 会得到"0.01 度的圆"，单位无意义
cities_m = cities.to_crs('EPSG:3857')
print('\n--- 重投影后（坐标变成大数，正常）---')
print(cities_m.geometry.iloc[0])     # POINT (1303xxxx 3740xxxx) 米


# ---------- 3. buffer：画 10 公里缓冲区 ----------
# 点 buffer 成圆；线 buffer 成条带；面 buffer 是外扩
buf = cities_m.geometry.buffer(10000)        # 10000 米 = 10 公里
print('\n--- 10km 缓冲区面积（应接近 π·10² ≈ 314 km²）---')
print((buf.area / 1e6).round(2), 'km²')


# ---------- 4. distance：城市间距离 ----------
d_hf_xc = cities_m.geometry.iloc[0].distance(cities_m.geometry.iloc[1])
d_xc_wh = cities_m.geometry.iloc[1].distance(cities_m.geometry.iloc[2])
print(f'\n合肥→宣城: {d_hf_xc/1000:.1f} km')
print(f'宣城→芜湖: {d_xc_wh/1000:.1f} km')


# ---------- 5. 对比：在 4326 里 buffer 没意义 ----------
# 在度坐标系里 buffer(0.01) 出来的"面积"单位是"平方度"，无法解释
buf_deg = cities.geometry.buffer(0.01)
print('\n--- 4326 里 buffer(0.01) 的"面积"---')
print(buf_deg.area, '平方度（无意义单位，别这么用）')


# ---------- 自己动手 ----------
# 1. 把 buffer 改成 5000 米和 20000 米，看面积是不是 4 倍和 16 倍关系（πr²）
# 2. 用 .distance() 算合肥→芜湖的距离，三个距离中哪段最长
# 3. to_crs('EPSG:32651') 换成 UTM 51N 投影，buffer 10km 的面积和 3857 差多少
