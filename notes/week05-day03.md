# Week 5 Day 3 — 布局：flexbox + 响应式

## 今天学什么

两个布局技能，让页面在不同屏幕上都好看：

1. **flexbox** —— 现代布局主力，替代 inline-block
2. **@media 响应式** —— 手机屏幕自动调整

## flexbox 核心（3 个属性记住就够）

```css
display: flex;              /* 开启 flex 布局 */
justify-content: center;    /* 主轴（横向）对齐：center 居中 */
gap: 20px;                  /* 项之间间距，替代 margin */
flex-direction: column;     /* 改成竖排（默认 row 横排） */
```

和 Day 2 的 `inline-block` 对比：
- inline-block 要用 margin 控间距，间距对齐靠猜
- flexbox 用 gap 控间距，justify-content 控对齐，精确又简单
- flexbox 能自动换行（flex-wrap）、能竖排（flex-direction: column）

## @media 响应式

```css
@media (max-width: 600px) {
    /* 屏幕宽度 < 600px 时，里面的规则生效 */
    nav ul { flex-direction: column; }
}
```

意思：屏幕窄到 600px 以下（手机），导航从横排变竖排。

## 今天改了什么

**`style.css`** 两处改动：

1. **nav 从 inline-block 升级到 flexbox**：
   - `display: flex` + `justify-content: center` + `gap: 20px`
   - 视觉效果和之前一样（横排居中），但底层更灵活
2. **新增 @media 响应式段**（文件末尾）：
   - 手机屏幕时：导航变竖排、边距减小、标题缩小

## 详细步骤（3 步，精简版）

### 第 1 步：刷新看 flexbox
刷新浏览器。导航看起来和昨天一样——横排居中。但底层从 inline-block 换成了 flexbox。

### 第 2 步：缩小窗口看响应式（重点）
把浏览器窗口慢慢拖窄。**到 600px 以下时**：
- 导航从横排变竖排
- 卡片间距变小
- 标题字号缩小
- 页面边距减小

这就是响应式——一套代码，电脑和手机都好看。

### 第 3 步：改断点实验
把 style.css 末尾 `@media (max-width: 600px)` 的 600 改成 900。
刷新，把窗口拖到 800px 宽——响应式提前生效了（因为 800 < 900）。
改回 600。

## 验收标准

- [ ] 刷新后导航还是横排居中（flexbox 生效）
- [ ] 拖窄窗口到手机宽度，导航变竖排（@media 生效）
- [ ] 能说清 flexbox 比 inline-block 好在哪（gap + justify-content + flex-direction）
- [ ] 改过 @media 的断点值并看到变化

## 为什么只用 flexbox 不学 float/grid

- **float**：2010 年前的布局方式，现在只用来文字环绕图片，不做布局了
- **grid**：二维布局（行列同时控），比 flexbox 强但复杂
- **flexbox**：一维布局（一次控一行或一列），覆盖 90% 场景，先学这个

grid 等做作品集页面（Day 4）如果需要两列再学。今天 flexbox 够用。

## 提交

```bash
cd /e/Dota/projects/geospatial-learning
git add .
git commit -m "feat: week05 day3 练习（flexbox 导航 + 响应式布局）"
git push
```
