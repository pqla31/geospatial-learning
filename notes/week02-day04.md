# Week 2 · Day 4 —— 时间序列与 pandas 绘图

> Week 2 收官。做完今天，pandas 四块核心（表格 → 筛选 → 分组 → 时间序列）就齐了，下周进 GeoPandas。

昨天用 `groupby('month')` 按月份分组——但 `month` 那一列是从字符串切片抠出来的 `'04'` `'05'`，不是真时间。今天学怎么把日期列变成**真正的时间类型**，然后用时间索引做更多事。

遥感数据天然带时间维度：同一站点不同日期的观测、同一像元不同时相的反射率。pandas 把日期做成时间索引后：

- 按月/季/年自动重采样（`resample`）
- 用日期字符串切片取一段（`df.loc['2026-05':'2026-07']`）
- `.dt` 访问器提取年/月/星期几

再加上 pandas 自带 `.plot()` 直接出图（底层就是上周学的 matplotlib），"读 CSV → 处理时间 → 画折线"这条链路是遥感时序分析的最小完整流程。

复用 `week02-pandas/stations.csv` 那 12 行。时间预算 1.5 小时。

---

## 17_timeseries.py —— 时间序列基础（约 40 分钟）

要求：

```python
import pandas as pd

df = pd.read_csv('week02-pandas/stations.csv')

# ---------- 0. 看原始类型 ----------
print(df['date'].dtype)          # object = 字符串，还不是时间

# ---------- 1. to_datetime：字符串转时间 ----------
df['date'] = pd.to_datetime(df['date'])   # '2026-04' -> 2026-04-01
print(df['date'].dtype)          # datetime64[ns]

# ---------- 2. set_index + sort_index：建时间索引 ----------
df = df.set_index('date').sort_index()
# 有了时间索引，能用日期字符串切片：
print(df.loc['2026-05':'2026-07'])    # 取 5-7 月，两端都含

# ---------- 3. 取时间成分 ----------
# 索引是时间时，直接用 .month / .year（不需要 .dt）
print(df.index.month)             # [4 4 4 5 5 5 6 6 6 7 7 7]
print(df.index.year.unique())     # [2026]

# .dt 访问器用在普通列上（不是索引）：
df_col = df.reset_index()
print(df_col['date'].dt.month_name().head())   # April April ...

# ---------- 4. resample：按月重采样 ----------
# resample = groupby 的时间版。'ME'=月末(Month End), 'QE'=季末(Quarter End)
# 3 站每月各 1 条，resample('ME').mean() = 每月 3 站均值
print(df[['ndvi', 'elevation']].resample('ME').mean())

# ---------- 5. resample 按季 ----------
print(df[['ndvi']].resample('QE').mean())   # 4 个月 -> 2 个季度
```

要点自查：
- `to_datetime` 是把字符串变成 `datetime64[ns]` 类型的关键步骤。不变，后面 `resample` 和日期切片都用不了。
- `set_index('date')` 后，`date` 从"普通列"变成"行标签"。取它用 `df.index`，不是 `df['date']`。
- **`resample('M')` 和 `groupby(df.index.month)` 结果一样吗？** 数值一样，但 `resample` 输出的索引是月末日期（`2026-04-30`），`groupby` 输出的是数字（`4`）。`resample` 是为时间序列设计的，能直接接 `.plot()` 出时间轴。
- `df.loc['2026-05':'2026-07']` 两端都含——和 `iloc` 的"不含尾"不同，这是**标签切片**的规则。

---

## 18_plot_timeseries.py —— pandas 绘图（约 50 分钟）

要求：

```python
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('week02-pandas/stations.csv')
df['date'] = pd.to_datetime(df['date'])

# ---------- 1. pivot_table：长表转宽表 ----------
# 原表 12 行（长格式）：每行一个站一个月
# pivot 后 4 行 × 3 列（宽格式）：行=月份，列=站名，值=ndvi
wide = df.pivot_table(index='date', columns='station', values='ndvi')
print(wide)

# ---------- 2. pandas .plot() 画折线 ----------
# pandas 的 .plot() 底层就是 matplotlib，每列一条线
ax = wide.plot(figsize=(8, 4), marker='o', linewidth=2)
ax.set_title('三站点 NDVI 月际变化（2026 年 4-7 月）')
ax.set_xlabel('月份'); ax.set_ylabel('NDVI')
ax.set_ylim(0, 1); ax.grid(alpha=0.3); ax.legend(title='站点')
fig = ax.figure
fig.tight_layout()
fig.savefig('week02-pandas/ndvi_timeseries.png', dpi=150)

# ---------- 3. 月均值柱状图 ----------
monthly = df.groupby('date')['ndvi'].mean()
ax2 = monthly.plot(kind='bar', figsize=(8, 4), color='#2e8b57')
ax2.set_title('NDVI 月均值（3 站平均）')
ax2.set_xlabel('月份'); ax2.set_ylabel('NDVI 均值')
ax2.set_ylim(0, 1); ax2.grid(alpha=0.3, axis='y')
ax2.set_xticklabels([d.strftime('%Y-%m') for d in monthly.index], rotation=0)
fig2 = ax2.figure
fig2.tight_layout()
fig2.savefig('week02-pandas/ndvi_monthly_bar.png', dpi=150)
```

要点自查：
- `pivot_table(index='date', columns='station', values='ndvi')` 把长表转宽表——这是画"每站一条线"必须的前置步骤。`plot()` 默认每列画一条线，所以要把站名变成列。
- pandas 的 `.plot()` 返回的就是 matplotlib 的 `ax` 对象，上周学的 `set_title` / `set_xlabel` / `grid` / `legend` 全部照常用。等于免费拿到一层封装。
- `kind='bar'` 画柱状图，`kind='scatter'` 画散点，不传 `kind` 默认折线。
- x 轴标签 `strftime('%Y-%m')` 是把时间格式化成 `2026-04` 这种字符串，不然 x 轴会显示 `2026-04-01 00:00:00` 一长串。

---

## 验收标准（四条全中才算过）

1. 能说清 `resample('M')` 和 `groupby(month)` 的区别——前者要时间索引、按时间周期分组、输出时间索引；后者按普通列分组、输出数值索引
2. `pivot_table` 转出来的宽表，行是 4 个月、列是 3 个站、值是 ndvi
3. 折线图：三条线 4-7 月都是上升的（夏季植被茂盛），合肥-01 整条线最低（城市+低海拔）
4. 两张 PNG 保存到 `week02-pandas/`，能打开

---

## 收工命令

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week02 day4 练习（时间序列与 pandas 绘图）"
git push
```

---

## Week 2 收官

做完今天，pandas 四块核心全齐：

| Day | 主题 | 核心动作 |
|---|---|---|
| 1 | 表格入门 | `read_csv` / `head` / `dtypes` / `to_csv` |
| 2 | 选择筛选 | `loc` / `iloc` / 布尔筛选 |
| 3 | 分组聚合 | `groupby` / `agg` / `sort_values` |
| 4 | 时间序列 | `to_datetime` / `set_index` / `resample` / `plot` |

下周 Week 3 进 **GeoPandas**——`GeoDataFrame = DataFrame + 几何列`。这四周学的全部直接复用，只是多了一列 `geometry` 存点/线/面。今天到这。
