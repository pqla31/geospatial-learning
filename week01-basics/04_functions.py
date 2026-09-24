def calc_ndvi(nir, red):
    return (nir - red) / (nir + red)


def classify(ndvi):
    if ndvi > 0.4:
        return '植被茂密'
    elif ndvi > 0.2:
        return '稀疏植被'
    elif ndvi > 0:
        return '裸土/建筑'
    else:
        return '水体'


# 三组样例数据：同一个函数被重复调用三次，这就是函数的意义
samples = [
    ('农田', 0.45, 0.08),
    ('建筑', 0.30, 0.28),
    ('水体', 0.05, 0.12),
]

for name, nir, red in samples:
    ndvi = calc_ndvi(nir, red)
    print(f'{name}: NDVI={ndvi:.2f}  地类：{classify(ndvi)}')

# 也可以接用户输入
nir = float(input('请输入近红外反射率：'))
red = float(input('请输入红光反射率：'))
my_ndvi = calc_ndvi(nir, red)
print(f'NDVI值是{my_ndvi:.4f}，类型是{classify(my_ndvi)}')
