courses = ['高等数学', 'GIS原理', '遥感导论', 'Python程序设计', '测量学']
courses.append('数据结构')
courses.remove('测量学')

for i, c in enumerate(courses, 1):
    print(f'{i}. {c}')

even = [n for n in range(1, 21) if n % 2 == 0]
print(even)

scores = {'GIS原理': 91, '遥感导论': 77, 'Python程序设计': 93}
for name, score in scores.items():
    print(f'{name}: {score}')