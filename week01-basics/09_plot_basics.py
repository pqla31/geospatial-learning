import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2*np.pi,200)
y1 = np.sin(x)
y2 = np.cos(x)
fig,ax = plt.subplots(figsize=(8,4),dpi=100)
ax.plot(x, y1, label="sin", color="blue", linewidth=2)
ax.plot(x, y2, label="cos", color="orange", linewidth=2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("sin and cos")
ax.set_xlim(0,2*np.pi)
ax.set_ylim(-1.5,1.5)
ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi])
ax.legend(loc='upper right')
ax.grid(True,linestyle='--',alpha=0.3)
fig.tight_layout()
fig.savefig("sin_cos.png",dpi=150,bbox_inches='tight')
plt.show()

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']   # 中文标题，不配就是方框
plt.rcParams['axes.unicode_minus'] = False

# 1 折线图
months = list(range(1, 13))
ndvi_month = [0.12, 0.15, 0.28, 0.45, 0.62, 0.71,
              0.75, 0.70, 0.55, 0.38, 0.22, 0.14]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, ndvi_month, marker='o', color='green', label='NDVI 月均值')
ax.set_title('某地 NDVI 年内变化')
ax.set_xlabel('月份'); ax.set_ylabel('NDVI')
ax.set_xticks(months); ax.grid(alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig('week01-basics/plot_line.png', dpi=150)
plt.show()

# 2 散点图
np.random.seed(0)
elev = np.random.uniform(100, 1200, 30)
cover = np.clip(80 - 0.05 * elev + np.random.normal(0, 8, 30), 0, 100)
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(elev, cover, c=cover, cmap='RdYlGn', edgecolor='k', s=60)
ax.set_title('高程与植被覆盖度关系')
ax.set_xlabel('高程 (m)'); ax.set_ylabel('植被覆盖度 (%)')
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('week01-basics/plot_scatter.png', dpi=150)
plt.show()

# 3 柱状图
classes = ['耕地', '林地', '草地', '水体', '建设用地', '裸土']
area = [28.5, 34.2, 15.8, 6.4, 10.1, 5.0]
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(classes, area, color=['#f6c85f', '#2e8b57', '#9acd32', '#4a90d9', '#b07aa1', '#c1440e'])
ax.set_title('各土地类型面积占比')
ax.set_xlabel('地类'); ax.set_ylabel('面积占比 (%)')
ax.grid(alpha=0.3, axis='y')
fig.tight_layout(); fig.savefig('week01-basics/plot_bar.png', dpi=150)
plt.show()