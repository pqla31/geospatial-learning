def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('请输入数字，例如 0.45')

nir = read_float('近红外反射率：')
red = read_float('红光反射率：')

if nir + red == 0:
    print('波段和为零，无法计算')
else:
    ndvi = (nir - red) / (nir + red)
    print(f'NDVI = {ndvi:.2f}')