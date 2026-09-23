school = '合肥工业大学'
major = '地球信息科学与技术'
year = 2025
enrolled = True

print(f'我是{school}{major}专业，{year}年入学，在读：{enrolled}')
print(type(school), type(year), type(enrolled))

from datetime import date
days_left = (date(2029, 6, 30) - date.today()).days
print(f'距离毕业还有 {days_left} 天')