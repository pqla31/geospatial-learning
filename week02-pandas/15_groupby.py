# Week 2 Day 3 —— groupby：分组统计
# 对应任务单：notes/week02-day03.md
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')
print('--- 原始表 ---')
print(df)


# ---------- 1. 单列分组 + 单统计量 ----------
print('\n--- 每个站的 ndvi 均值 ---')
print(df.groupby('station')['ndvi'].mean())


# ---------- 2. 单列分组 + 多统计量 ----------
print('\n--- 每个站的 ndvi：mean/max/min/count ---')
print(df.groupby('station')['ndvi'].agg(['mean', 'max', 'min', 'count']))


# ---------- 3. 分组后对多列统计 ----------
print('\n--- 每个站的 ndvi 均值 + elevation 均值 ---')
print(df.groupby('station')[['ndvi', 'elevation']].mean())


# ---------- 4. size：每组几行 ----------
print('\n--- 每组行数（size） ---')
print(df.groupby('station').size())


# ---------- 5. 多列分组 ----------
df['month'] = df['date'].str[-2:]       # '2026-04' -> '04'
print('\n--- 按 station+month 分组的 ndvi 均值 ---')
print(df['month'])
print(df.groupby(['station', 'month'])['ndvi'].mean())
print (df.groupby('station')) 

# ---------- 自己动手 ----------
# 1. 单独 print df.groupby('station') 看输出是什么——记住它是个分组对象，不链统计方法就没数
# 2. 算每个站的 NDVI 标准差 std，看哪个站月际波动最大
print('\n' + str(df.groupby('station').agg(
    ndvi_std=('ndvi','std'))))
# 3. df.groupby('station')['elevation'].first() 和 .mean() 输出一样吗？想想为什么（高程每站固定）
print('\n' + str(df.groupby('station')['elevation'].first()))
print('\n' + str(df.groupby('station')['elevation'].mean()))