import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

nir = np.array([
    [0.45, 0.42, 0.40, 0.38],
    [0.30, 0.28, 0.32, 0.29],
    [0.05, 0.06, 0.04, 0.07],
    [0.50, 0.48, 0.46, 0.44],
    [0.35, 0.33, 0.31, 0.30],
    [0.10, 0.12, 0.09, 0.11],
])
red = np.array([
    [0.08, 0.09, 0.10, 0.11],
    [0.28, 0.27, 0.30, 0.28],
    [0.12, 0.13, 0.10, 0.14],
    [0.06, 0.07, 0.08, 0.09],
    [0.20, 0.19, 0.18, 0.17],
    [0.11, 0.13, 0.10, 0.12],
])

ndvi = (nir - red) / (nir + red)

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
fig.colorbar(im, ax=ax, label='NDVI')
ax.set_title('NDVI 空间分布')
ax.axis('off')
fig.tight_layout()
fig.savefig('week01-basics/ndvi_map.png', dpi=150)
plt.show()
