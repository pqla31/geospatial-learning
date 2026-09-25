# Week 1 · Day 4 —— matplotlib：把数字画成图

昨天算出了 NDVI 矩阵，但一堆数字看不出分布。今天把它画出来——这是遥感工作的日常动作：算完必须可视化，否则你不知道自己算得对不对。

环境里已有 matplotlib 3.9.4，中文字体 Microsoft YaHei / SimHei 都可用。

时间预算 1.5 小时，目录 `week01-basics/`。

---

## 09_plot_basics.py —— 三种最常用图（约 40 分钟）

要求：

1. **折线图**：模拟某地 12 个月的 NDVI 月均值，画一条折线
   ```python
   months = list(range(1, 13))
   ndvi_month = [0.12, 0.15, 0.28, 0.45, 0.62, 0.71,
                 0.75, 0.70, 0.55, 0.38, 0.22, 0.14]
   plt.plot(months, ndvi_month, marker='o')
   ```
2. **散点图**：模拟 30 个采样点的「高程 vs 植被覆盖度」，看是否有关系
3. **柱状图**：把 6 个地类的面积占比画成柱子

三个图都必须有：标题、x 轴标签、y 轴标签、网格 `plt.grid(alpha=0.3)`。

要点自查：
- 每张图之间要 `plt.figure()` 新建画布，否则三个图会叠在同一张上
- 结尾用 `plt.savefig('week01-basics/plot_basics.png', dpi=150)` 保存，**dpi 别用默认的 72**，会很糊
- 保存要在 `plt.show()` 之前（如果写了 show 的话）

---

## 10_ndvi_map.py —— 把 NDVI 矩阵画成热力图（约 50 分钟）

复用昨天 `08_numpy_ndvi.py` 里那组 6×4 的波段数据，算出 NDVI 后渲染。

**中文显示必须先配这两行**，否则标题全是方框：

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']   # 或 'SimHei'
plt.rcParams['axes.unicode_minus'] = False              # 让负号正常显示
```

要求：

1. 用 `plt.imshow()` 渲染 NDVI 矩阵：
   ```python
   plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
   ```
   `RdYlGn` 是红-黄-绿，正好对应「低-中-高」的植被含义；`vmin/vmax` 固定量程，否则不同图之间颜色没法比较
2. 加 `plt.colorbar(label='NDVI')` 显示色带刻度
3. 加中文标题（如「NDVI 空间分布」）、`plt.axis('off')` 去掉坐标轴刻度
4. 保存为 `week01-basics/ndvi_map.png`，dpi=150
5. 额外挑战：用 `np.where` 把 NDVI 分成三档（水体 -1 / 裸土 0 / 植被 1），再用 `cmap='Set1'` 画一张离散分级图，跟连续图对比着看

要点自查：
- 图里第三行应该是**深红**（负值，水体），第一、四行应该是**深绿**（高值，植被）——跟昨天的数字对得上才算画对
- 保存后自己打开 png 看一眼，别只信代码没报错

---

## 验收标准（三条全中才算过）

1. 能画出带标题、轴标签、图例的折线图并保存成 png
2. 能把 NDVI 矩阵渲染成带 colorbar 的热力图，且颜色高低方向正确
3. 知道 `vmin/vmax` 是干嘛的（提示：不设的话每次按该图自身的最值拉伸，两张图就不可比了）

---

## 收工命令

```bash
git add .
git commit -m "feat: week01 day4 练习（matplotlib 绘图）"
git push
```

注意：`.gitignore` 里已经排除了 `*.tif/*.shp` 等大数据，png 不在排除范围内，可以正常提交——图也是成果的一部分，让仓库主页有图比全是代码好看得多。
