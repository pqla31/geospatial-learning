# Week 2 Day 4 —— 时间序列基础
# 对应任务单：notes/week02-day04.md
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')
print('--- 原始表（date 是字符串）---')
print(df)
print('\ndate 列类型:', df['date'].dtype)       # object = 字符串


# ---------- 1. to_datetime：字符串转时间 ----------
df['date'] = pd.to_datetime(df['date'])        # '2026-04' -> 2026-04-01
print('\n--- 转换后 ---')
print(df['date'].dtype)                         # datetime64[ns]
print(df.head())


# ---------- 2. set_index + sort_index：建时间索引 ----------
df = df.set_index('date').sort_index()
print('\n--- 以 date 为索引 ---')
print(df)

# 有了时间索引，能用日期字符串切片（两端都含）
print('\n--- df.loc["2026-05":"2026-07"] 取 5-7 月 ---')
print(df.loc['2026-05':'2026-07'])


# ---------- 3. 取时间成分 ----------
# 当 date 是索引时，直接用 .month / .year（不需要 .dt）
print('\n--- df.index.month ---')
print(df.index.month)
print('\n--- df.index.year.unique() ---')
print(df.index.year.unique())

# .dt 访问器用在普通列上（不是索引）
df_col = df.reset_index()
print('\n--- df_col["date"].dt.month_name() ---')
print(df_col['date'].dt.month_name().head())


# ---------- 4. resample：按月重采样 ----------
# resample = groupby 的时间版。'ME'=月末（Month End）
# 3 站每月各 1 条，resample('ME').mean() = 每月 3 站均值
print('\n--- resample("ME").mean() 每月 3 站均值 ---')
print(df[['ndvi', 'elevation']].resample('ME').mean())


# ---------- 5. resample 按季 ----------
# 'Q'=季末。4 个月 -> 2 个季度
print('\n--- resample("Q").mean() 每季均值 ---')
print(df[['ndvi']].resample('Q').mean())


# ---------- 自己动手 ----------
# 1. df.loc["2026-06"] 只取 6 月——试试用单个日期切片（不传区间）
# 2. resample("M").agg(["mean","max","min"]) 看每月极值范围
# 3. df.reset_index()["date"].dt.dayofweek 看每条观测是星期几（0=周一，6=周日）
