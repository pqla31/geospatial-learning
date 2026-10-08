import numpy as np

print([1, 2, 3] * 2)              # 列表 * 2：复制一份接在后面
print(np.array([1, 2, 3]) * 2)    # 数组 * 2：每个元素都乘 2

arr = np.array([1, 2, 3, 4, 5.3])
print(arr)
print(type(arr))
print(arr.shape)
print(arr.dtype)
print(arr.ndim)

a = np.arange(12).reshape(3, 4)
print(a)
print(a.shape)
print(a.ndim)
print(a.size)

print(a[1, 2])          # 第 2 行第 3 列
print(a[0, :])          # 第 1 行全部
print(a[:, 1])          # 第 2 列全部
print(a[0:2, 1:3])      # 前两行 × 中间两列

print(a.max(axis=0))    # 每列的最大值

print('聚合:', a.mean(), a.max(), a.min(), a.sum(), a.std())
print('axis=0:', a.mean(axis=0))
print('axis=1:', a.mean(axis=1))

print('布尔矩阵:')
print(a > 5)
print('取出的值:', a[a > 5])
print('True 占比:', (a > 5).mean())
