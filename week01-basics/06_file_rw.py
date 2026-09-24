samples = [
    ('农田', 0.45, 0.08),
    ('建筑', 0.30, 0.28),
    ('水体', 0.05, 0.12),
]

with open('week01-basics/ndvi_result.txt', 'w', encoding='utf-8') as f:
    for name, nir, red in samples:
        ndvi = (nir - red) / (nir + red)
        f.write(f'{name},{ndvi:.2f}\n')

with open('week01-basics/ndvi_result.txt', encoding='utf-8') as f:
    print(f.read())