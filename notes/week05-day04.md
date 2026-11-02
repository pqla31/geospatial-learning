# Week 5 Day 4 — 作品集页面 + Week 5 封板

## 今天学什么

把前三天的 HTML + CSS + flexbox 整合成一个**作品集页面**（portfolio.html）。
新增一个布局技能：**CSS Grid**（二维网格布局，比 flexbox 更适合卡片排列）。

## Grid vs Flexbox

| | Flexbox | Grid |
|---|---|---|
| 维度 | 一维（一行或一列） | 二维（行列同时控） |
| 适合 | 导航、工具栏、单行/单列 | 卡片网格、图片墙、表格布局 |
| 关键属性 | `justify-content` `gap` `flex-direction` | `grid-template-columns` `gap` |

今天的项目卡片用 grid 两列：
```css
.projects {
    display: grid;
    grid-template-columns: repeat(2, 1fr);  /* 2 列等宽 */
    gap: 20px;
}
```
`repeat(2, 1fr)` = 2 列，每列占 1 份等宽（1fr = 1 fraction）。

## 今天的文件

### portfolio.html（新建）— 作品集页面

结构：
- **Hero 区域**：大标题 + 简介 + 8 个技能标签（Python/NumPy/pandas/...）
- **项目网格**：4 个项目卡片（Week 1-4），grid 两列排列，每个卡片有图+标题+描述
- **学习时间线**：表格，5 周内容 + 脚本数
- **关于**：学习方向 + 目标 + 仓库链接

### style.css — 新增 Day 4 段

- `.hero` 渐变背景 + 大内边距
- `.skills` + `.tag` flexbox 标签云
- `.projects` grid 两列 + `.project-card` 卡片样式
- `transition` + `:hover` 卡片悬停上浮动画
- `table` 表格样式 + 行悬停高亮
- 响应式：手机时 grid 变一列

## 详细步骤（3 步）

### 第 1 步：打开 portfolio.html 看效果
用浏览器打开 `week05-frontend/portfolio.html`（或在 VS Code 里预览）。
应该看到：蓝色渐变 hero + 技能标签 + 4 张项目卡片两列排列 + 时间线表格。

### 第 2 步：体验卡片悬停动画
鼠标移到项目卡片上——卡片上浮 4px、投影变深。这是 `transition: transform 0.2s` + `:hover` 的效果。

### 第 3 步：拖窄窗口看响应式
拖窄到手机宽度：项目卡片从两列变一列，hero 标题缩小。

## 验收标准

- [ ] portfolio.html 打开有完整作品集效果
- [ ] 4 张项目卡片 grid 两列排列
- [ ] 鼠标悬停卡片有上浮动画
- [ ] 表格有边框线和行悬停高亮
- [ ] 拖窄窗口卡片变一列（响应式 grid）
- [ ] 技能标签横排居中、自动换行

## Week 5 四天回顾

| Day | 主题 | 核心 |
|---|---|---|
| 1 | HTML 基础 | 文档结构、常用标签、语义化 |
| 2 | CSS 基础 | 选择器、盒模型、颜色字体 |
| 3 | flexbox + 响应式 | `display:flex` + `@media` |
| 4 | Grid + 作品集 | `grid-template-columns` + 卡片网格 + 动画 |

## 学期阶段一全部目标达成

三个目标全齐：
1. **Python 地学** — 能跑通 NDVI 分区统计完整流程（Week 1-4）
2. **GitHub** — 35 个脚本 + 2 个网页 + 15 张图，持续提交
3. **前端 HTML/CSS** — 能手写静态页面，含响应式布局（Week 5）

## 提交

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week05 day4 作品集页面（grid 卡片网格 + hero + 时间线）；Week 5 封板"
git push
```

## 下一步

学期阶段一结束。下一阶段（大二下 2027.02 起）方向：
- 前端进阶：JavaScript（让页面有交互）
- WebGIS：Leaflet/Cesium 地图前端
- 感知启动期（2027.03）：PyTorch + C++（15 个月加速方案第二阶段）

但那是下学期的事。现在这学期的三个目标已经全部达成了。
