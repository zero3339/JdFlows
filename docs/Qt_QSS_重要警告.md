# ⚠️ Qt QSS 重要警告

> **必读**：Qt Style Sheets (QSS) ≠ CSS3

---

## 🚨 核心警告

### Qt QSS 基于 CSS2.1，不支持大部分 CSS3 特性！

如果你有 Web 前端经验，请**忘记大部分 CSS3 知识**。Qt QSS 是一个**功能受限的 CSS 子集**。

---

## ❌ 不支持的 CSS3 特性

### 1. Flexbox 布局
```css
/* ❌ 这在 Qt 中不工作 */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

**Qt 正确方式**：
```python
# ✓ 使用 Qt 布局管理器
layout = QHBoxLayout()
layout.addStretch()
layout.addWidget(widget)
layout.addStretch()
```

### 2. Grid 布局
```css
/* ❌ 不支持 */
.container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 QGridLayout
layout = QGridLayout()
layout.addWidget(widget1, 0, 0)
layout.addWidget(widget2, 0, 1)
```

### 3. Transform 变换
```css
/* ❌ 不支持 */
.rotate {
    transform: rotate(45deg);
    transform: scale(1.5);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 QTransform
from PyQt6.QtGui import QTransform
transform = QTransform().rotate(45)
widget.setTransform(transform)
```

### 4. Transition 过渡动画
```css
/* ❌ 不支持 */
.button {
    transition: all 0.3s ease;
}

.button:hover {
    transform: translateY(-2px);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 QPropertyAnimation
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

anim = QPropertyAnimation(widget, b"pos")
anim.setDuration(300)
anim.setStartValue(QPoint(0, 0))
anim.setEndValue(QPoint(0, -2))
anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
anim.start()
```

### 5. Keyframe 动画
```css
/* ❌ 不支持 */
@keyframes slide {
    from { left: 0; }
    to { left: 100px; }
}

.animated {
    animation: slide 1s;
}
```

**Qt 正确方式**：
```python
# ✓ 使用 QPropertyAnimation
anim = QPropertyAnimation(widget, b"geometry")
anim.setDuration(1000)
anim.setStartValue(QRect(0, 0, 100, 100))
anim.setEndValue(QRect(100, 0, 100, 100))
anim.start()
```

### 6. Box Shadow
```css
/* ❌ 不支持（或支持极差）*/
.card {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 QGraphicsDropShadowEffect
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

shadow = QGraphicsDropShadowEffect()
shadow.setBlurRadius(15)
shadow.setColor(QColor(0, 0, 0, 50))
shadow.setOffset(0, 2)
widget.setGraphicsEffect(shadow)
```

### 7. Calc() 函数
```css
/* ❌ 不支持 */
.element {
    width: calc(100% - 50px);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 Python 计算
parent_width = self.width()
widget.setFixedWidth(parent_width - 50)
```

### 8. CSS 变量
```css
/* ❌ 不支持 */
:root {
    --primary-color: #0066FF;
}

.button {
    background-color: var(--primary-color);
}
```

**Qt 正确方式**：
```python
# ✓ 使用 Python 变量 + f-string
PRIMARY_COLOR = "#0066FF"

stylesheet = f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
}}
"""
widget.setStyleSheet(stylesheet)
```

### 9. Media Queries
```css
/* ❌ 不支持 */
@media (max-width: 768px) {
    .sidebar {
        display: none;
    }
}
```

**Qt 正确方式**：
```python
# ✓ 使用 resizeEvent
def resizeEvent(self, event):
    if event.size().width() < 768:
        self.sidebar.hide()
    else:
        self.sidebar.show()
```

### 10. Position (absolute/fixed)
```css
/* ❌ 不支持 */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
}
```

**Qt 正确方式**：
```python
# ✓ 使用 setGeometry 或布局
widget.setGeometry(0, 0, width, height)

# 或使用层叠窗口
overlay = QWidget(parent)
overlay.setGeometry(parent.rect())
```

---

## ✅ Qt QSS 支持的属性

### 完整支持列表

```css
/* 颜色属性 */
color: #000000;
background-color: #FFFFFF;
border-color: #CCCCCC;

/* 尺寸属性 */
width: 100px;
height: 50px;
min-width: 80px;
max-width: 200px;
min-height: 30px;
max-height: 100px;

/* 间距属性 */
padding: 10px;
padding-left: 5px;
padding-right: 5px;
padding-top: 8px;
padding-bottom: 8px;
margin: 10px;

/* 边框属性 */
border: 2px solid #000000;
border-width: 1px;
border-style: solid;  /* solid, dashed, dotted, none */
border-radius: 4px;   /* 圆角（有限支持）*/
border-left: 1px solid #CCC;

/* 字体属性 */
font-family: "Arial", sans-serif;
font-size: 14px;
font-weight: bold;    /* normal, bold, 100-900 */
font-style: italic;   /* normal, italic, oblique */

/* 文本属性 */
text-align: left;     /* left, right, center */
text-decoration: underline;  /* none, underline, line-through */

/* 背景属性 */
background: #FFF;
background-image: url(:/images/bg.png);
background-repeat: no-repeat;
background-position: center;
```

### 选择器支持

```css
/* 基础选择器 */
QWidget { }           /* 类型选择器 */
#myWidget { }         /* ID 选择器 */
.myClass { }          /* 类选择器 */

/* 伪类选择器 */
:hover { }            /* 悬停 */
:pressed { }          /* 按下 */
:disabled { }         /* 禁用 */
:enabled { }          /* 启用 */
:focus { }            /* 焦点 */
:checked { }          /* 选中（复选框/单选框）*/

/* 伪元素选择器 */
::item { }            /* 列表项 */
::indicator { }       /* 复选框指示器 */
::handle { }          /* 滚动条把手 */
::chunk { }           /* 进度条填充 */
::branch { }          /* 树形视图分支 */

/* 后代选择器 */
QDialog QPushButton { }   /* 后代 */
QWidget > QLabel { }      /* 直接子元素 */
```

---

## 📋 常见错误对照表

| Web CSS3 写法 | Qt QSS 正确写法 | 说明 |
|--------------|----------------|------|
| `display: flex` | `QHBoxLayout()` | 使用布局管理器 |
| `transform: rotate()` | `QTransform().rotate()` | 使用 Qt 变换 |
| `transition: all 0.3s` | `QPropertyAnimation` | 使用 Qt 动画 |
| `box-shadow: 0 2px 4px` | `QGraphicsDropShadowEffect` | 使用图形效果 |
| `calc(100% - 50px)` | Python 计算 | 运行时计算 |
| `var(--color)` | f-string 变量 | Python 字符串格式化 |
| `@media query` | `resizeEvent()` | 重写事件处理 |
| `position: absolute` | `setGeometry()` | 直接设置位置 |
| `z-index: 10` | `raise_()` / `lower()` | 改变层叠顺序 |
| `opacity: 0.5` | `setWindowOpacity(0.5)` | 使用 Qt 方法 |

---

## 💡 最佳实践

### 1. 样式与布局分离

```python
# ✓ 好的做法
# 布局用 Qt 布局管理器
layout = QVBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)

# 样式用 QSS
widget.setStyleSheet("""
    QWidget {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
    }
""")
```

### 2. 动画用 Qt 动画框架

```python
# ✓ 好的做法
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

def animate_fade_in(widget):
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(300)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    anim.start()
```

### 3. 复杂效果用 QPainter

```python
# ✓ 好的做法
def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # 自定义绘制
    painter.setBrush(QColor("#0066FF"))
    painter.drawRoundedRect(self.rect(), 8, 8)
```

### 4. 主题切换用 Python

```python
# ✓ 好的做法
def apply_theme(self, theme_name):
    if theme_name == "dark":
        bg = "#1E1E1E"
        fg = "#FFFFFF"
    else:
        bg = "#FFFFFF"
        fg = "#000000"
    
    stylesheet = f"""
        QWidget {{
            background-color: {bg};
            color: {fg};
        }}
    """
    self.setStyleSheet(stylesheet)
```

---

## 🔍 调试技巧

### 检查 QSS 是否生效

```python
# 打印当前样式表
print(widget.styleSheet())

# 检查属性
print(widget.property("background-color"))

# 强制刷新样式
widget.style().unpolish(widget)
widget.style().polish(widget)
widget.update()
```

### 测试简单样式

```python
# 先用简单样式测试
widget.setStyleSheet("background-color: red;")

# 如果红色显示了，说明选择器正确
# 然后逐步添加其他属性
```

---

## 📚 参考资源

- **官方 QSS 参考**: https://doc.qt.io/qt-6/stylesheet-reference.html
- **支持的属性列表**: https://doc.qt.io/qt-6/stylesheet-customizing.html
- **示例集合**: https://doc.qt.io/qt-6/stylesheet-examples.html

---

## ⚠️ 总结

### 记住这三点

1. **Qt QSS ≠ CSS3** - 仅支持 CSS2.1 的子集
2. **布局/动画/特效** - 使用 Qt 原生 API，不要用 CSS
3. **仅用 QSS 做样式** - 颜色、字体、边框、间距

### 当你想用 CSS3 时

```
问自己：这是样式（颜色/字体/边框）还是布局/动画？

样式 → 用 QSS ✓
布局 → 用 QBoxLayout/QGridLayout ✓
动画 → 用 QPropertyAnimation ✓
特效 → 用 QPainter/QGraphicsEffect ✓
```

---

**牢记**：Qt 是桌面框架，不是 Web 浏览器！ 🎯
