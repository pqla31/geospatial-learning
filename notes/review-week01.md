# Week 1 复习卡（Day 1–3）

> 断档 13 天后的快速回顾。这里只放「会用到的」和「踩过的坑」，不放解释性长文。
> 卡住时查这里，比回去翻教程快。

---

## Day 1 · 基础语法

### 变量与类型

```python
school = '合肥工业大学'     # str
year = 2025                # int
ndvi = 0.7321              # float
enrolled = True            # bool（不加引号！）
print(type(school), type(year), type(enrolled))
```

踩过的坑：

| 写法 | 实际是什么 | 正确写法 |
|---|---|---|
| `2025-9.1` | 减法，得 `2015.9`（float） | `'2025-09'`（字符串） |
| `'True'` | 四个字符的字符串 | `True`（布尔值，不加引号） |

### f-string

```python
print(f'我是{school}{major}专业，{year}年入学')
print(f'{ndvi:.2f}')      # 保留 2 位小数
print(f'{r:.1f}%')        # 1 位小数 + 百分号
print(f'{x:,.2f}')        # 千分位 + 2 位小数
print(f'{0.7321:.1%}')    # 自动 ×100 → 73.2%
```

想输出字面花括号要写两个：`f'{{字面}}'`。

### 列表

```python
courses = ['高等数学', 'GIS原理', '遥感导论']
courses.append('数据结构')     # 末尾加
courses.remove('测量学')       # 按值删

for i, c in enumerate(courses, 1):   # 1 = 序号从 1 开始（默认 0）
    print(f'{i}. {c}')
```

### 列表推导式

```python
even = [n for n in range(1, 21) if n % 2 == 0]   # [2, 4, ..., 20]
```

读法：对 `range(1,21)` 里的每个 n，满足 `n % 2 == 0` 就收进新列表。

### 字典

```python
scores = {'GIS原理': 91, '遥感导论': 77}
for name, score in scores.items():   # .items() 同时取键和值
    print(f'{name}: {score}')
```

### 条件判断

```python
if ndvi > 0.4:
    kind = '植被茂密'
elif ndvi > 0.2:
    kind = '稀疏植被'
elif ndvi > 0:
    kind = '裸土/建筑'
else:
    kind = '水体'
```

### 日期

```python
from datetime import date
days_left = (date(2029, 6, 30) - date.today()).days   # 整数天
```

- 两个日期相减得到 `timedelta`，加 `.days` 才是整数
- 月份别写 `06`，前导零会语法报错

---

## Day 2 · 组织代码

### 函数：用 return，不用 print

```python
def calc_ndvi(nir, red):
    return (nir - red) / (nir + red)      # 交出数值，不负责打印

def classify(ndvi):
    if ndvi > 0.4:
        return '植被茂密'
    ...
    return '水体'
```

**核心规矩：一个函数只干一件事。** 算归算、判归判、打印是调用方的事。
这样 `classify(ndvi)` 才能被塞进 f-string，也才能被别的函数继续拿去用。

`print` 只是把东西显示在屏幕上，函数外部拿不到；`return` 才是把结果交出去。

### 异常处理：输入校验的标准姿势

```python
def read_float(prompt):
    while True:
        try:
            return float(input(prompt))   # 成功 → 直接返回并跳出循环
        except ValueError:
            print('请输入数字，例如 0.45')
```

除零单独拦一道：

```python
if nir + red == 0:
    print('波段和为零，无法计算')
else:
    ndvi = (nir - red) / (nir + red)
```

### 文件读写

```python
with open('week01-basics/ndvi_result.txt', 'w', encoding='utf-8') as f:
    f.write(f'{name},{ndvi:.2f}\n')

with open('week01-basics/ndvi_result.txt', encoding='utf-8') as f:
    print(f.read())
```

三个必记：

1. `encoding='utf-8'` **必须加**，不然中文在 Windows 上乱码
2. `'w'` 覆盖写（每次清空重写）／`'a'` 追加写（接着后面写），别混
3. 路径是**相对于敲命令时所在的目录**，不是脚本文件所在目录 →
   脚本要在仓库根目录跑：`python week01-basics/06_file_rw.py`

---

## Day 3 · NumPy（进行中）

### 建数组与看属性

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(type(arr), arr.shape, arr.dtype)      # (5,)  int64

a = np.arange(12).reshape(3, 4)             # 3 行 4 列
print(a.shape, a.ndim)                      # (3, 4)  2
print(a.size)                               # 12
```

`shape` 是 `(行数, 列数)`。

### 索引与切片

```python
a[1, 2]        # 第 2 行第 3 列（索引从 0 开始）
a[0, :]        # 第 1 行全部
a[0:2, 1:3]    # 前两行 × 中间两列
```

### 列表 vs 数组（Day 3 的核心）

| 写法 | 结果 | 含义 |
|---|---|---|
| `[1, 2, 3] * 2` | `[1, 2, 3, 1, 2, 3]` | 复制一份接在后面 |
| `np.array([1, 2, 3]) * 2` | `[2 4 6]` | 每个元素各乘 2 |

**列表是「装东西的盒子」，数组是「一整块数字」。** 盒子只能一个个拿出来操作（所以要写 for 循环），整块数字可以整体加减乘除。

所以 NDVI 才能一行算完：

```python
ndvi = (nir - red) / (nir + red)     # nir / red 是数组 → 一次算出整幅图
```

同样这行代码，如果 nir、red 是 Python 列表，会直接 `TypeError`。

### 聚合统计

```python
a.mean(), a.max(), a.min(), a.sum(), a.std()
```

### axis：记住「压掉哪一维」

**`axis=n` 就是把第 n 维压掉。**

以 3 行 4 列的 `a` 为例：

| 写法 | 压掉 | 结果个数 | 每个是什么 |
|---|---|---|---|
| `a.mean(axis=0)` | 行 | 4 个 | 每一列的均值（跨 3 行算） |
| `a.mean(axis=1)` | 列 | 3 个 | 每一行的均值（跨 4 列算） |

不用背，用「压掉」这个规则现场推。

### 布尔筛选 / 掩膜

```python
a[a > 5]                 # 取出所有大于 5 的元素，得到一维数组
(ndvi > 0.4)             # 得到一块 True/False，形状和 ndvi 一样
(ndvi > 0.4).mean()      # True 的占比 → 乘 100 就是植被覆盖率
```

这一步是全文件的精髓：**比较运算作用在整块数组上，返回同样形状的布尔数组；`.mean()` 就是 True 的比例。**

---

## 自测 10 题

先自己答，答不上再翻上面的正文。

1. `2025-9.1` 的结果是什么类型？为什么不能用来表示入学时间？
2. `'True'` 和 `True` 有什么区别？
3. 写一个 f-string，把 `0.7321` 输出成 `73.2%`。
4. `enumerate(courses, 1)` 里的 `1` 是什么意思？去掉会怎样？
5. 一个函数里 `print` 和 `return` 有什么区别？为什么 `classify()` 用 `return`？
6. `while True` + `try` + `return` 这个组合，为什么能防住用户输入字母？
7. `open(..., 'w')` 换成 `open(..., 'a')` 有什么不同？`encoding='utf-8'` 不加会怎样？
8. 脚本在仓库根目录跑，和 `cd` 进 `week01-basics` 再跑，写出来的 txt 位置有什么差别？
9. `[1,2,3]*2` 和 `np.array([1,2,3])*2` 的结果分别是什么？
10. 3×4 的数组，`a.mean(axis=0)` 得到几个数？每个数是什么含义？

<details>
<summary>答案</summary>

1. 减法，结果是 float `2015.9`。要表示入学时间用字符串 `'2025-09'`。
2. `'True'` 是四个字符组成的字符串，不能参与 `if` 判断；`True` 是布尔值。
3. `print(f'{0.7321:.1%}')`
4. 序号从 1 开始计。去掉默认从 0 开始。
5. `print` 只显示在屏幕上，函数外部拿不到值；`return` 把结果交出去。用 `return` 才能把分类名塞进 f-string 或传给别的函数。
6. 转换失败抛 `ValueError` 被 `except` 接住，打印提示后 `while` 再循环一次重新问；成功就直接 `return` 跳出。
7. `'w'` 每次清空重写，`'a'` 在文件末尾接着写。不加 `encoding='utf-8'` 中文会乱码。
8. 相对路径相对的是「当前工作目录」。根目录跑 → txt 生成在 `week01-basics/`（因为路径里写了前缀）；`cd` 进子目录再跑 → 会在 `week01-basics/week01-basics/` 下找路径，找不到目录直接报错。
9. `[1, 2, 3, 1, 2, 3]`（重复拼接）；`[2 4 6]`（逐元素相乘）。
10. 4 个。每个是「一列的均值」——把 3 行压掉，跨行算出来。

</details>

---

## 常用命令

```bash
conda activate gis                                  # 进环境
python week01-basics/07_numpy_array.py              # 在仓库根目录跑
python                                              # 进交互模式，试语法
exit()                                              # 退出交互模式

git status                                          # 看改动
git add .
git commit -m "feat: week01 day3 练习（NumPy）"
git push
```
