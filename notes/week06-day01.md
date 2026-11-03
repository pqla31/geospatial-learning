# Week 6 Day 1 — JavaScript 基础：让页面动起来

## 方向说明

学期阶段一三目标全齐后，现在启动下学期内容。方向是 **JavaScript**，理由：

1. 前端三件套还差 JS（HTML/CSS 已学完），这是自然衔接
2. JS 是 WebGIS（Leaflet 地图）的前置——不学 JS 直接上地图会卡
3. 12-01 起加 LeetCode（每天 30 分钟，用 Python），和 JS 并行不冲突
4. PyTorch 感知等 2027.02 寒假后启动——交接文档明确的时间点，不提前

Week 6-7 学 JS 基础，Week 8-9 进 WebGIS（Leaflet 地图）。

## 今天学什么

**JavaScript** 是前端三件套的第三件，也是唯一真正的编程语言。
HTML 是结构（骨架），CSS 是样式（皮肤），JS 是交互（肌肉）—— 点击、输入、动画、数据加载全归它管。

你会 Python，JS 的逻辑你已经懂了（变量、函数、条件、循环）。今天重点是**语法差异**和**怎么和 HTML 连起来**。

## JS 怎么放进 HTML

```html
<script>
    // JS 代码写在这里
    console.log('hello');
</script>
```
`<script>` 标签通常放 `</body>` 前面（页面加载完再跑 JS）。

## 和 Python 的语法对比（贴在桌上）

| 功能 | Python | JavaScript |
|---|---|---|
| 输出 | `print(x)` | `console.log(x)` |
| 变量 | `x = 1` | `let x = 1` |
| 常量 | `PI = 3.14`（约定） | `const PI = 3.14` |
| 相等 | `==` | `===`（严格相等，不转类型） |
| 条件 | `if x > 5:` | `if (x > 5) { }` |
| 函数 | `def f(x):` | `function f(x) { }` |
| 单行注释 | `#` | `//` |
| 字符串 | `'hello'` / `"hello"` | `'hello'` / `"hello"`（一样） |

**最重要的区别：`===` vs `==`**
- `===` 严格相等：`1 === '1'` → false（数字不等于字符串）
- `==` 宽松相等：`1 == '1'` → true（自动转类型，容易出 bug）
- **永远用 `===`，别用 `==`**

## 今天的 4 个核心概念

**1. `console.log()` = Python 的 `print()`**
输出在浏览器的 F12 → Console 面板，不是页面上。

**2. `document.querySelector('#id')` 选元素**
和 CSS 选择器完全一样：`'#title'` 选 id、`'.card'` 选 class、`'h1'` 选标签。

**3. `.textContent = '新文字'` 改内容**
选中元素后改它的文字。这就是"JS 让页面动起来"的本质。

**4. `.addEventListener('click', function)` 绑定事件**
点击按钮时自动运行函数。这是交互的入口。

## 今天的文件

### 01_js_basics.html — 第一个 JS 交互页面

- 一个按钮，点击计数 +1
- 点击 5/10/20 次时标题文字和颜色变化
- console.log 输出每次点击（F12 Console 看）
- 复用 Week 5 的 style.css（`<link>` 引用）

## 详细步骤（5 步）

### 第 1 步：打开页面
双击 `week06-javascript/01_js_basics.html` 用浏览器打开。
看到一个白色卡片：标题"Hello JavaScript" + 计数 0 + 按钮。

### 第 2 步：点按钮看交互
点"点击我"按钮。每点一次：
- 数字 +1
- console.log 输出"第 N 次点击"
点到 5 次：标题变红"点了 5 次！"
点到 10 次：标题变绿"十次了！厉害"
点到 20 次：标题变灰"别点了，都 20 次了"

### 第 3 步：打开 F12 Console（重点）
按 F12 → 切到 Console 面板。
你能看到 `console.log` 的输出："页面加载完成"、"第 1 次点击"……
**Console 就是 JS 的终端**——和 Python 的 print 输出到终端一样。

在 Console 里直接敲 `count` 回车——能看到当前计数值。
这就是 JS 的交互式调试：Console 里可以直接敲代码运行。

### 第 4 步：对照源码看逻辑
VS Code 打开 `01_js_basics.html`，找到 `<script>` 标签。
对照看：
- `let count = 0` → 计数器变量
- `document.querySelector('#btn')` → 选按钮
- `btn.addEventListener('click', function() { ... })` → 点击时做什么
- `countEl.textContent = count` → 改页面数字

### 第 5 步：做自选练习
在 `<script>` 里加一个"重置"按钮：
1. 在 HTML 里按钮后面加：`<button id="reset">重置</button>`
2. 在 JS 里加：
```javascript
const resetBtn = document.querySelector('#reset');
resetBtn.addEventListener('click', function() {
    count = 0;
    countEl.textContent = 0;
    titleEl.textContent = 'Hello JavaScript';
    titleEl.style.color = '';
    console.log('已重置');
});
```
保存 → 刷新 → 点重置按钮看效果。

## 验收标准

- [ ] 点按钮计数 +1，页面数字实时变化
- [ ] F12 Console 能看到 console.log 输出
- [ ] Console 里直接敲 `count` 能看当前值
- [ ] 点到 5/10/20 次标题变化
- [ ] 能说清 querySelector / textContent / addEventListener 分别干什么
- [ ] （可选）加了重置按钮

## 提交

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week06 day1 练习（JavaScript 基础 + 点击交互）"
git push
```

## 一个坑

**改了 JS 刷新没变化**——和 CSS 一样是缓存问题，`Ctrl+F5` 强制刷新。
或者 F12 → Network 面板勾 "Disable cache" 永久跳过缓存（开发时开着）。
