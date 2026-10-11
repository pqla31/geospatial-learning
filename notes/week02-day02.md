# Week 2 · Day 2 —— DataFrame 的选择与条件筛选

昨天会建表、会存读 CSV 了。今天学 pandas 里**用得最频繁**的一块：把"符合条件的行"挑出来。

遥感里日常就是这种活：

- "把 NDVI > 0.5 的像元挑出来统计面积"
- "挑 2026 年 7 月那一批观测"
- "找出高程 > 500 m 的所有站点"

本质全是同一件事——**生成一个布尔 Series（True/False），塞回 `df[...]` 里取行**。

复用昨天 `week02-pandas/stations.csv` 那 12 行数据。

时间预算 1.5 小时。

---

## 13_loc_iloc.py —— 按标签 vs 按位置取行（约 40 分钟）

pandas 取行有两条路，新手最容易混：

| | `loc` | `iloc` |
|---|---|---|
| 取的是 | **标签**（index 上的名字） | **位置**（第几个，从 0 数） |
| 切片尾 | **含**（`0:2` 含 2） | **不含**（`0:2` 不含 2，跟 Python 切片一致） |

要求：

```python
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')

# ---------- loc：按标签 ----------
print(df.loc[0])                          # 第 0 行（标签就是 0）
print(df.loc[0:2, ['station', 'date', 'ndvi']])   # 标签 0~2，含 2；选三列

# ---------- iloc：按位置 ----------
print(df.iloc[0])                          # 第 0 个位置
print(df.iloc[0:2, [0, 4]])                # 位置 0~1，不含 2；第 0、4 列（跟上面 loc[0:2] 对比：同样写 0:2，iloc 少一行）

# ---------- 把 station 设成索引后，loc 就能按站名取 ----------
df_idx = df.set_index('station')
print(df_idx.loc['宣城-01'])               # 直接按站名取，不用记它在第几行
print(df_idx.loc[['宣城-01', '合肥-01']])  # 取两个站
```

要点自查：
- `df.loc[0:2]` 出来 **3 行**（0、1、2，含 2），`df.iloc[0:2]` 出来 **2 行**（0、1，不含 2）。这是最常错的点。
- `iloc` 的列参数只能用整数位置（`[0, 4]`），不能用列名；`loc` 只能用列名。
- `set_index` 不改变原 df（除非加 `inplace=True`），它返回一个新表，所以要赋值给变量。

---

## 14_filter.py —— 条件筛选（约 50 分钟）

核心一句话：**`df[布尔 Series]` = 取出 True 对应的行**。所有条件筛选都是这个套路。

要求：

```python
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')

# ---------- 1. 单条件 ----------
high = df[df['ndvi'] > 0.6]
print('NDVI > 0.6 的：')
print(high[['station', 'date', 'ndvi']])
print('共', len(high), '行')

# ---------- 2. 多条件：& 且、| 或 ----------
# 注意：每个条件必须用括号包住，且用 & 不能用 and
print('\n宣城-01 且 NDVI > 0.5 的：')
print(df[(df['station'] == '宣城-01') & (df['ndvi'] > 0.5)])

print('\n合肥-01 或 7 月的：')
print(df[(df['station'] == '合肥-01') | (df['date'] == '2026-07')])

# ---------- 3. isin：在不在一个集合里 ----------
print('\n两个指定站点的：')
print(df[df['station'].isin(['宣城-01', '合肥-01'])])

# ---------- 4. 字符串方法 .str ----------
print('\n 7 月的观测（date 以 07 结尾）：')
print(df[df['date'].str.endswith('07')])

# ---------- 5. ~ 取反 ----------
print('\n NDVI 不超过 0.5 的：')
print(df[~(df['ndvi'] > 0.5)])

# ---------- 6. 选完再统计 ----------
print('\n 高植被（NDVI>0.5）那批的均值：', df[df['ndvi'] > 0.5]['ndvi'].mean())
```

要点自查（这几个坑今天必须踩明白）：
- 多条件每个子条件**必须加括号**：`(df['a'] > 1) & (df['b'] < 2)`。漏括号 pandas 会报 `cannot determine truth value`，因为 `&` 的优先级比 `>` `==` 高。
- 用的是 **`&` 和 `|`，不是 `and` `or`**。`and` 是给单个布尔值用的，pandas 里要对整个 Series 做逐元素运算，必须用位运算符。
- `df['ndvi'] > 0.6` 单独 print 出来看看——它就是一个 12 行的 True/False 序列，`df[它]` 才是取行。**理解这一步是理解全部筛选的关键**。
- `.str` 是 pandas 字符串列的专属方法族（`contains` / `startswith` / `endswith`），数值列没有。

---

## 验收标准（三条全中才算过）

1. 说得出 `loc` 和 `iloc` 的两个区别（标签 vs 位置、切片含不含尾）
2. 能写出多条件筛选，每个子条件都加了括号、用 `&` / `|` 而不是 `and` / `or`
3. 能解释 `df[df['ndvi'] > 0.6]` 这一句发生了什么（先生成布尔 Series，再拿它当索引取行）

---

## 收工命令

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week02 day2 练习（DataFrame 选择与条件筛选）"
git push
```
