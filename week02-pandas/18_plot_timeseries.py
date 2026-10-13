# Week 2 Day 4 —— pandas 绘图：NDVI 时序折线与柱状图
# 对应任务单：notes/week02-day04.md
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
print('--- 宽表（行=月份，列=站名）---')
print(wide)


# ---------- 2. pandas .plot() 画折线 ----------
# pandas 的 .plot() 底层就是 matplotlib，每列一条线
ax = wide.plot(figsize=(8, 4), marker='o', linewidth=2)
ax.set_title('三站点 NDVI 月际变化（2026 年 4-7 月）')
ax.set_xlabel('月份')
ax.set_ylabel('NDVI')
ax.set_ylim(0, 1)
ax.grid(alpha=0.3)
ax.legend(title='站点')

fig = ax.figure
fig.tight_layout()
fig.savefig('week02-pandas/ndvi_timeseries.png', dpi=150)
print('\n图已保存：week02-pandas/ndvi_timeseries.png')


# ---------- 3. 月均值柱状图 ----------
monthly = df.groupby('date')['ndvi'].mean()
print('\n--- 每月 3 站 NDVI 均值 ---')
print(monthly)

ax2 = monthly.plot(kind='bar', figsize=(8, 4), color='#2e8b57')
ax2.set_title('NDVI 月均值（3 站平均）')
ax2.set_xlabel('月份')
ax2.set_ylabel('NDVI 均值')
ax2.set_ylim(0, 1)
ax2.grid(alpha=0.3, axis='y')
# x 轴标签：把时间格式化成 '2026-04'，不然显示一长串时间戳
ax2.set_xticklabels([d.strftime('%Y-%m') for d in monthly.index], rotation=0)

fig2 = ax2.figure
fig2.tight_layout()
fig2.savefig('week02-pandas/ndvi_monthly_bar.png', dpi=150)
print('图已保存：week02-pandas/ndvi_monthly_bar.png')


# ---------- 自己动手 ----------
# 1. 把折线的 marker='o' 换成 's'（方块）或 '^'（三角），看哪个更清楚
# 2. ax.set_ylim(0, 0.8) 缩小 y 轴范围，看曲线是不是显得更陡
# 3. pivot_table(index='station', columns='date', values='ndvi') 反转行列再 .plot()，
#    看图变成什么样（行=站、列=月，每站一条线变成每站一张子图了吗？）
