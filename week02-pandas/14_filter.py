# Week 2 Day 2 —— 条件筛选：把符合条件的行挑出来
# 对应任务单：notes/week02-day02.md
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')
print('--- 原始表 ---')
print(df)


# ---------- 0. 先看清楚"布尔 Series"长什么样 ----------
mask = df['ndvi'] > 0.6
print('\n--- df["ndvi"] > 0.6 这个布尔 Series 本体 ---')
print(mask)                   # 一列 True/False，长度 12
print('dtype:', mask.dtype)


# ---------- 1. 单条件 ----------
high = df[df['ndvi'] > 0.6]
print('\n--- NDVI > 0.6 的 ---')
print(high[['station', 'date', 'ndvi']])
print('共', len(high), '行')


# ---------- 2. 多条件 &（且）、|（或）----------
# 每个子条件必须加括号，用 & 不能用 and
print('\n--- 宣城-01 且 NDVI > 0.5 ---')
print(df[(df['station'] == '宣城-01') & (df['ndvi'] > 0.5)])

print('\n--- 合肥-01 或 7 月的 ---')
print(df[(df['station'] == '合肥-01') | (df['date'] == '2026-07')])


# ---------- 3. isin：在某集合里 ----------
print('\n--- 站点在 [宣城-01, 合肥-01] 里 ---')
print(df[df['station'].isin(['宣城-01', '合肥-01'])])


# ---------- 4. 字符串方法 .str ----------
print('\n--- 7 月的（date 以 07 结尾）---')
print(df[df['date'].str.endswith('07')])


# ---------- 5. ~ 取反 ----------
print('\n--- NDVI 不超过 0.5 的（取反）---')
print(df[~(df['ndvi'] > 0.5)])


# ---------- 6. 选完再统计 ----------
sub = df[df['ndvi'] > 0.5]
print(f'\n--- 高植被（NDVI>0.5）共 {len(sub)} 行，NDVI 均值 {sub["ndvi"].mean():.3f} ---')
print('\n')
print('\n')
# ---------- 自己动手 ----------
# 1. 改成：取「宣城-02 且 6 月以后（含6月）」的行。日期是字符串"2026-06"，可以直接比较大小 df['date'] >= '2026-06'
# 2. 算一下「合肥-01」4 个月的 NDVI 均值（提示：先筛选 station，再取 ndvi 列 .mean()）
hf = (df[df['station'] == '合肥-01'] ['ndvi'].mean())
print(f"「合肥-01」4 个月的 NDVI 均值:{hf:.3f}")
# 3. 用 .str.contains('宣城') 取所有站名带"宣城"的行——这比 isin 列举省事
