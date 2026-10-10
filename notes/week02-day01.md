# Week 2 · Day 1 —— pandas：把「表」接进 Python

昨天处理的 NDVI 是一个纯数字矩阵。但真实工作里，数据长这样：

| station | date | lon | lat | ndvi | elevation |
|---|---|---|---|---|---|
| 宣城-01 | 2026-04 | 118.76 | 30.94 | 0.62 | 42 |
| 合肥-01 | 2026-04 | 117.23 | 31.82 | 0.48 | 31 |

站点名、经纬度、日期、观测值——这是**表**。野外采样记录、气象站点台账、导出的 Excel，全是这个形态。

pandas 就是 Python 里处理表的库。为什么必须学它：**geopandas 的 GeoDataFrame 本质上就是 DataFrame 多一列几何**——你不熟 pandas，下周学 shapefile 属性表操作会直接卡住。

环境里已有 pandas 2.3.1。

时间预算 1.5 小时，目录 `week02-pandas/`。

---

## 11_pandas_intro.py —— DataFrame 到底是个啥（约 40 分钟）

要求：

1. **Series**：一维、带标签的数组。跟 NumPy 的 ndarray 唯一区别就是每个值有个名字（索引标签）
   ```python
   import pandas as pd

   s = pd.Series([0.62, 0.71, 0.55],
                 index=['站点A', '站点B', '站点C'],
                 name='ndvi')
   print(s)
   print(s['站点B'])     # 按标签取值，不是按位置
   print(s.mean(), s.max())
   ```
2. **DataFrame**：把几个等长的 Series 按列拼起来，就是一张表
   ```python
   df = pd.DataFrame({
       'station': ['宣城-01', '宣城-02', '宣城-03', '合肥-01'],
       'lon':     [118.76, 118.81, 118.70, 117.23],
       'lat':     [30.94, 30.90, 30.99, 31.82],
       'ndvi':    [0.62, 0.71, 0.55, 0.48],
   })
   print(df)
   ```
3. **六个查看动作**，每个都 print 出来，看清楚各自给什么信息：
   ```python
   print(df.head(2))      # 前 n 行，默认 5 行
   print(df.shape)        # (行数, 列数)
   print(df.columns)      # 列名
   print(df.dtypes)       # 每列的数据类型
   print(df.info())       # 行数/列数/类型/有没有缺失
   print(df.describe())   # 数值列的统计摘要
   ```

要点自查：
- `df.shape` **不带括号**（属性），`df.head()` **带括号**（方法）。跟 NumPy 的 `ndarray.shape` 一个道理，写错会报 `tuple is not callable`。
- `describe()` 只统计数值列，字符串列自动跳过——所以 `station` 不会出现在它的输出里。
- `dtypes` 里 `int64` / `float64` 是数字，`object` 基本就是字符串。

---

## 12_station_csv.py —— 存成 CSV 再读回来（约 50 分钟）

要求：

1. 用 `pd.DataFrame({...})` 造一张 **12 行**的表：3 个站点 × 4 个月份，列为
   `station` / `date` / `lon` / `lat` / `ndvi` / `elevation`
   （值自己编，合理就行：宣城 4→7 月 NDVI 逐步升高，合肥略低）
2. **存成 CSV**：
   ```python
   df.to_csv('week02-pandas/stations.csv', index=False, encoding='utf-8-sig')
   ```
3. **读回来**：
   ```python
   df2 = pd.read_csv('week02-pandas/stations.csv')
   print(df2.head())
   print(df2.shape)
   ```
4. **取列 / 取行**：
   ```python
   print(df2['ndvi'])               # 单列 → Series
   print(df2[['station', 'ndvi']])  # 多列 → DataFrame（双层方括号）
   print(df2['ndvi'].mean())        # 整列统计
   print(df2.nlargest(3, 'ndvi'))   # ndvi 最大的 3 行
   ```
5. **新增一列**：按 NDVI 分等级
   ```python
   def grade(v):
       if v < 0.2:
           return '裸土'
       elif v < 0.5:
           return '低植被'
       else:
           return '植被'

   df2['level'] = df2['ndvi'].apply(grade)
   print(df2['level'].value_counts())
   ```

要点自查（这两个坑今天必须记住）：
- `index=False` **必须加**。不加的话 CSV 里会多出一列没有名字的 0/1/2 行号，下次 `read_csv` 读回来变成 `Unnamed: 0` 垃圾列。
- `encoding='utf-8-sig'` **必须加**。不加的话 Excel 打开中文全是乱码——Python 自己读没问题，是 Excel 认不出无 BOM 的 UTF-8。写 `utf-8` 不够，必须是 `utf-8-sig`。
- `apply(grade)` 里函数名**后面不要加括号**。你传的是"函数本身"，不是"调用它的结果"。写成 `apply(grade())` 会直接报错。

`stations.csv` 只有 12 行，刻意让它进仓库——别人 clone 下来就能直接跑你的脚本，不用先造数据。

---

## 验收标准（三条全中才算过）

1. 能从字典造出 DataFrame，并且说得出 `shape` / `dtypes` / `describe` 各自看到的是什么
2. 能把表存成 CSV 再读回来，读回来的 `columns` 里**没有** `Unnamed: 0`，且用 Excel 打开中文不乱码
3. 能用 `apply` 加出一列分级结果，并 `value_counts()` 出每级各有多少行

---

## 收工命令

```bash
git add .
git commit -m "feat: week02 day1 练习（pandas 入门与 CSV 读写）"
git push
```
