# Week 6 Day 2 — DOM 数据渲染：用 JS 动态生成 HTML

## 今天学什么

Day 1 是"点按钮改一个文字"，今天是"用数据批量生成 HTML 元素"——这是数据驱动页面的核心。

把 Week 2 的 3 个站点 NDVI 数据写在 JS 数组里，用 forEach 遍历生成卡片。

## 和 Python 的对比

| 功能 | Python | JavaScript |
|---|---|---|
| 列表/数组 | `[1, 2, 3]` | `[1, 2, 3]`（一样） |
| 遍历 | `for item in list:` | `array.forEach(function(item) { })` |
| 字符串插值 | `f'hello {name}'` | `` `hello ${name}` ``（反引号包裹） |
| 创建元素 | `soup.new_tag('div')` | `document.createElement('div')` |
| 写内容 | `tag.string = '文字'` | `element.innerHTML = '文字'` |
| 添加到页面 | `parent.append(tag)` | `parent.appendChild(element)` |

## 4 个核心概念

**1. 数组 + forEach**
```javascript
const stations = [{name:'合肥-01', ndvi:0.488}, ...];
stations.forEach(function(s) { /* 每个站点跑一次 */ });
```

**2. createElement 创建元素**
```javascript
const card = document.createElement('div');  // 创建了但还不在页面上
```

**3. 模板字符串 `` ` ${变量} ` ``**
反引号（键盘左上角 ~ 那个键）包裹，`${变量}` 插值，和 Python f-string 一样。
```javascript
card.innerHTML = `<h3>${s.name}</h3><p>NDVI: ${s.ndvi}</p>`;
```

**4. appendChild 加到页面**
```javascript
container.appendChild(card);  // 把创建的元素加到页面上显示
```

## 今天的文件

### 02_dom_data.html — 站点 NDVI 卡片

- 3 个站点的数据写在 JS 数组里
- forEach 遍历生成 project-card 样式的卡片（复用 Week 5 CSS）
- NDVI 值根据高低显示不同颜色（绿/黄/红）
- 点击卡片弹出详情（alert）
- F12 Console 看数据加载日志

## 步骤

1. **打开 02_dom_data.html**——看到 3 张站点卡片，NDVI 值按颜色区分
2. **点卡片**——弹出详情框（alert）
3. **F12 Console**——看 forEach 遍历日志
4. **改数据实验**：在 stations 数组里加一个站点 `{name:'巢湖站', ndvi:-0.3, nir:0.02, type:'水体'}`，刷新看多一张红色卡片
5. **提交**：
```bash
git add .
git commit -m "feat: week06 day2 练习（DOM 数据渲染）"
git push
```

## 一个坑

**模板字符串必须用反引号 `` ` ``，不是单引号 `'`。** 反引号在键盘左上角 Esc 下面那个键。写成 `'<h3>${s.name}</h3>'` 不会插值，`${s.name}` 会原样显示。
