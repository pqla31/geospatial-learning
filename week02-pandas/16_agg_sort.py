# Week 2 Day 3 —— agg 多函数聚合 + sort_values 排序
# 对应任务单：notes/week02-day03.md
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')
print('--- 原始表 ---')
print(df)


# ---------- 1. agg 多函数 ----------
print('\n--- 每站 ndvi：mean/std/max/min ---')
print(df.groupby('station')['ndvi'].agg(['mean', 'std', 'max', 'min']))


# ---------- 2. 不同列用不同聚合（字典）----------
print('\n--- ndvi 给 mean+max，elevation 给 first ---')
print(df.groupby('station').agg({
    'ndvi': ['mean', 'max'],
    'elevation': 'first',
}))


# ---------- 3. sort_values 单列排序 ----------
print('\n--- ndvi 最大的 5 行（降序）---')
print(df.sort_values('ndvi', ascending=False).head(5))

print('\n--- ndvi 最小的 3 行（默认升序）---')
print(df.sort_values('ndvi').head(3))


# ---------- 4. sort_values 多列排序 ----------
print('\n--- 先按 station 升序，站内 ndvi 降序 ---')
print(df.sort_values(['station', 'ndvi'], ascending=[True, False]))


# ---------- 5. 分组统计后再排序 ----------
print('\n--- 每站 ndvi 均值，按均值降序 ---')
g = df.groupby('station')['ndvi'].mean().sort_values(ascending=False)
print(g)


# ---------- 6. 分组内排名 ----------
df['rank_in_station'] = df.groupby('station')['ndvi'].rank(ascending=False, method='min')
print('\n--- 每站内部 ndvi 排名 ---')
print(df.sort_values(['station', 'rank_in_station']))


# ---------- 自己动手 ----------
# 1. 把 agg(['mean','std','max','min']) 里的 std 去掉换成 median（中位数），看均值和中位数差多少
# 2. sort_values(['station','ndvi']) 不传 ascending，默认是什么？传 ascending=[False,True] 又是什么？
# 3. 用 rank(method='dense') 代替 method='min'，对比输出差异（并列名次处理不同）
