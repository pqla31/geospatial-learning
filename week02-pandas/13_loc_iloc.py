# Week 2 Day 2 —— loc vs iloc：按标签 vs 按位置取行
# 对应任务单：notes/week02-day02.md
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')
print('--- 原始表 ---')
print(df)
print('shape:', df.shape)


# ---------- loc：按标签取 ----------
# 默认 index 是 0,1,2,...（数字标签）
print('\n--- df.loc[0] 第 0 行 ---')
print(df.loc[0])

print("\n--- df.loc[0:2, ['station','date','ndvi']] 标签 0~2（含 2，共 3 行）---")
print(df.loc[0:2, ['station', 'date', 'ndvi']])


# ---------- iloc：按位置取 ----------
print('\n--- df.iloc[0] 第 0 个位置 ---')
print(df.iloc[0])

print('\n--- df.iloc[0:2, [0, 4]] 位置 0~1（不含 2，共 2 行），第 0、4 列 ---')
print(df.iloc[0:2, [0, 4]])


# ---------- 把 station 设成索引，loc 就能按站名取 ----------
df_idx = df.set_index('station')        # 不改原 df，返回新表
print('\n--- set_index 后按站名取 ---')
print(df_idx.loc['宣城-01'])
print('\n--- 取两个站 ---')
print(df_idx.loc[['宣城-01', '合肥-01']])


# ---------- 自己动手 ----------
# 1. 单独 print df.loc[0:2] 和 df.iloc[0:2]，数一数各几行，把这个区别记住
# 2. 试试 df.iloc[0:3, ['station','ndvi']]，会报什么错？iloc 的列参数只能用什么？
# 3. 用 df_idx.loc['宣城-01', 'ndvi'] 直接取出宣城-01 的 4 个月 NDVI（Series），算它的均值
