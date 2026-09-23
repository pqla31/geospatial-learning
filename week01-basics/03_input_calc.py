NIR=float(input("请输入接收近红外："))
RED=float(input("请输入红光："))
NDVI= (NIR - RED) / (NIR + RED)
if NDVI > 0.4:
    aaa=('植被茂密')
elif NDVI > 0.2:
    aaa=('稀疏植被')
elif NDVI > 0:
    aaa=('裸土/建筑')
else:
    aaa=('水体')
print(f'{NDVI:.4f},{aaa}')