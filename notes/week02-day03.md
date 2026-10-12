# Week 2 · Day 3 —— 分组聚合：groupby / agg / sort_values

昨天学了怎么"挑出符合条件的行"。今天学怎么"按某列分组，每组算个统计量"。

这是遥感属性表分析天天干的事：

- "按行政区算每个区的 NDVI 均值" → `df.groupby('行政区')['ndvi'].mean()`
- "按地类统计面积总和" → `df.groupby('地类')['面积'].sum()`
- "每个采样点每月的均值" → `df.groupby(['站点','月份'])['ndvi'].mean()`

本质就是三步：**分组（split）→ 每组算（apply）→ 拼回一张表（combine）**。

复用 `week02-pandas/stations.csv` 那 12 行。

时间预算 1.5 小时。

---

## 15_groupby.py —— groupby 基础（约 40 分钟）

要求：

```python
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')

# ---------- 1. 单列分组 + 单统计量 ----------
# 每个 station 的 ndvi 均值
print(df.groupby('station')['ndvi'].mean())

# ---------- 2. 单列分组 + 多统计量 ----------
print(df.groupby('station')['ndvi'].agg(['mean', 'max', 'min', 'count']))

# ---------- 3. 分组后对多列统计 ----------
# 每个 station 的 ndvi 均值 + elevation 均值
print(df.groupby('station')[['ndvi', 'elevation']].mean())

# ---------- 4. size：每组几行 ----------
print(df.groupby('station').size())     # 注意是 size() 不是 count()，size 数行数含空值

# ---------- 5. 多列分组 ----------
# 提取月份
df['month'] = df['date'].str[-2:]       # '2026-04' -> '04'
print(df.groupby(['station', 'month'])['ndvi'].mean())
```

要点自查：
- `groupby('station')` 本身不输出结果，它是个"分组对象"（DataFrameGroupBy）。要再链 `.mean()` / `.agg(...)` 才有数。新手常犯的错是只写 `df.groupby('station')` 然后 print 出来发现是个对象。
- `['ndvi']` 放在 `groupby` 后面是"分组后只对这一列算"；放在前面 `df[['ndvi','elevation']]` 是"先选列再分组"，两种写法都对，但语义不同。
- `size()` 数的是**行数**（含缺失值），`count()` 数的是**非缺失值个数**。今天没缺数据看不出区别，但要知道有这个差异。

---

## 16_agg_sort.py —— 多函数聚合与排序（约 50 分钟）

要求：

```python
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')

# ---------- 1. agg 多函数 ----------
print(df.groupby('station')['ndvi'].agg(['mean', 'std', 'max', 'min']))

# ---------- 2. 不同列用不同聚合（字典）----------
print(df.groupby('station').agg({
    'ndvi': ['mean', 'max'],
    'elevation': 'first',     # 高程每站固定，取第一个就行
}))

# ---------- 3. sort_values 单列排序 ----------
print(df.sort_values('ndvi', ascending=False).head(5))   # NDVI 最大的 5 行
print(df.sort_values('ndvi').head(3))                    # 最小的 3 行（默认升序）

# ---------- 4. sort_values 多列排序 ----------
# 先按 station 字母序，站内再按 ndvi 降序
print(df.sort_values(['station', 'ndvi'], ascending=[True, False]))

# ---------- 5. 分组统计后再排序 ----------
# 每站 NDVI 均值，按均值降序
g = df.groupby('station')['ndvi'].mean().sort_values(ascending=False)
print(g)

# ---------- 6. 分组内排名 ----------
df['rank_in_station'] = df.groupby('station')['ndvi'].rank(ascending=False, method='min')
print(df.sort_values(['station', 'rank_in_station']))
```

要点自查：
- `agg(['mean','max'])` 传的是**函数名字符串列表**，不是函数调用；`agg([mean, max])`（不引号）会报错，因为传的是函数对象但 pandas 认不全。
- 字典写法 `agg({'ndvi':['mean','max'], 'elevation':'first'})` 输出是**多级列索引**（列名变成 `('ndvi','mean')` 这种），看着乱但正常，记住每列是"原列名+函数名"两层。
- `sort_values` 的 `ascending` 传单值给单列排序；多列排序传**列表**，长度和排序列数对应。`ascending=[True, False]` = 第一列升序、第二列降序。
- `rank(method='min')` 里 `method` 控制并列名次怎么处理：`'min'` 是取最小名次（并列都给第1名），`'dense'` 是不跳号。今天数小看不出差别，知道有参数即可。

---

## 验收标准（三条全中才算过）

1. 能用 `groupby(单列)` 配 `agg(多函数)` 出一张分组统计表
2. 能用 `sort_values` 做单列和多列排序，并说清 `ascending` 传单值和传列表的区别
3. 能说出 `groupby('station')` 这一句执行后发生了什么（split：按 station 把 12 行切成 3 组；后面接 `.mean()` 才 apply+combine）

---

## 收工命令

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week02 day3 练习（分组聚合与排序）"
git push
```
