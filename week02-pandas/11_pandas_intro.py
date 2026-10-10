import pandas as pd


# ---------- 1. Series：一维、带标签的数组 ----------
# 跟 NumPy 的 ndarray 唯一区别：每个值有个名字（索引标签）
s = pd.Series([0.62, 0.71, 0.55],
              index=['站点A', '站点B', '站点C'],
              name='ndvi')

print('--- Series ---')
print(s)
print('按标签取 站点B:', s['站点B'])          # 注意：按标签取，不是按位置
print(f'均值 {s.mean():.3f} | 最大 {s.max():.3f}')


# ---------- 2. DataFrame：几列拼起来的一张表 ----------
# 1. 给 df 加一列 'elevation'（高程，自己编 4 个数），再 print(df.describe()) 看多了哪一行
df = pd.DataFrame({
    'elevation': [100, 120, 80, 50],
    'station': ['宣城-01', '宣城-02', '宣城-03', '合肥-01'],
    'lon':     [118.76, 118.81, 118.70, 117.23],
    'lat':     [30.94, 30.90, 30.99, 31.82],
    'ndvi':    [0.62, 0.71, 0.55, 0.48],
})

print('\n--- DataFrame ---')
print(df)


# ---------- 3. 六个查看动作，每个都看清楚给什么信息 ----------
print('\n--- head(2) 前两行 ---')
print(df.head(2))

print('\n--- shape (行数, 列数) ---')
print(df.shape)          # 属性，不带括号

print('\n--- columns 列名 ---')
print(df.columns)

print('\n--- dtypes 每列类型 ---')
print(df.dtypes)         # object = 字符串；int64/float64 = 数字

print('\n--- info() 概览 ---')
print(df.info())

print('\n--- describe() 数值列统计摘要 ---')
print(df.describe())     # 只统计数值列，station 不会出现在里面
print('\n')
print(df['ndvi'])


# 2. print(df['ndvi']) 看看单列长什么样——它的类型是 Series 还是 DataFrame？
# 3. 试试 print(df.shape()) 会报什么错，记住：属性不带括号，方法带括号
