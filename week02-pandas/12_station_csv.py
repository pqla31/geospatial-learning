import pandas as pd


# ---------- 1. 造一张 12 行的站点观测表（3 站点 × 4 个月） ----------
df = pd.DataFrame({
    'station':   ['宣城-01'] * 4 + ['宣城-02'] * 4 + ['合肥-01'] * 4,
    'date':      ['2026-04', '2026-05', '2026-06', '2026-07'] * 3,
    'lon':       [118.76] * 4 + [118.81] * 4 + [117.23] * 4,
    'lat':       [30.94] * 4 + [30.90] * 4 + [31.82] * 4,
    'ndvi':      [0.42, 0.55, 0.68, 0.74,
                  0.38, 0.51, 0.65, 0.71,
                  0.31, 0.44, 0.57, 0.63],
    'elevation': [42] * 4 + [58] * 4 + [31] * 4,
})

print('--- 原始表 ---')
print(df)
print('shape:', df.shape)


# ---------- 2. 存成 CSV ----------
# index=False    -> 不写行号列，否则读回来多一列 Unnamed: 0
# utf-8-sig      -> 带 BOM，Excel 打开中文才不乱码（写 utf-8 不行）
df.to_csv('week02-pandas/stations.csv', index=False, encoding='utf-8-sig')
print('\n已保存 week02-pandas/stations.csv')


# ---------- 3. 读回来 ----------
df2 = pd.read_csv('week02-pandas/stations.csv')
print('\n--- 读回来的列名 ---')
print(list(df2.columns))       # 这里如果出现 Unnamed: 0，说明上一步漏了 index=False
print('shape:', df2.shape)
print(df2.head())


# ---------- 4. 取列 / 取行 ----------
print('\n--- 单列 df2["ndvi"]（Series） ---')
print(df2['ndvi'])

print('\n--- 多列 df2[["station", "ndvi"]]（DataFrame，双层方括号） ---')
print(df2[['station', 'ndvi']])

print('\n--- 整列统计与排序 ---')
print(f'NDVI 均值 {df2["ndvi"].mean():.3f}')
print(df2.nlargest(3, 'ndvi'))     # NDVI 最大的 3 行


# ---------- 5. 新增一列：按 NDVI 分级 ----------
def grade(v):
    if v < 0.2:
        return '裸土'
    elif v < 0.5:
        return '低植被'
    else:
        return '植被'


# apply 里写函数名，不要加括号——传的是函数本身，不是调用结果
df2['level'] = df2['ndvi'].apply(grade)

print('\n--- 分级结果 ---')
print(df2[['station', 'date', 'ndvi', 'level']])

print('\n--- 每级各有多少行 ---')
print(df2['level'].value_counts())


# ---------- 自己动手 ----------
# 1. 把 stations.csv 用 Excel 打开，确认中文没乱码；再用记事本打开，确认没有多余的 0,1,2 列
# 2. 加一列 'temp'（气温，自己编 12 个数），统计每个站点的平均气温（提示：groupby 是 Day 3 的内容，
#    现在可以先用 df2[df2['station'] == '宣城-01']['temp'].mean() 这种笨办法）
# 3. 把 grade 的分级阈值改成 0.3 / 0.6，看看 value_counts 的结果怎么变
