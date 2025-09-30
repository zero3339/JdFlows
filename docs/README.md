# JDFlows

> 京东商品采集系统 | 极简黑白UI | Python + PyQt6 + Playwright

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 2. 运行UI演示
python demo_minimalist_ui.py

# 3. 运行主程序
python main.py
```

---

## 📖 文档导航

| 文档 | 大小 | 说明 | 适用对象 |
|-----|------|------|---------|
| **[开发指南.md](开发指南.md)** | 60.3KB | 完整开发流程和技术栈 | 全栈开发 ⭐ |
| [GUI优化补充指南.md](GUI优化补充指南.md) | 10.9KB | UI/UX优化和高级组件 | 前端进阶 |
| ⚠️ **[Qt_QSS_重要警告.md](Qt_QSS_重要警告.md)** | 必读 | Qt QSS ≠ CSS3 | **所有前端开发** ⚠️ |
| 📋 **[todos.md](todos.md)** | 45个主要任务 | 5阶段开发计划（12-17周） | **项目管理** 📋 |
| 🤖 **[AGENTS.md](AGENTS.md)** | AI代理 | AI编程代理简报包 | **AI开发工具** 🤖 |
| 🚨 **[FACTORY_AI_RULES.md](FACTORY_AI_RULES.md)** | 强制规则 | Factory AI代理行为约束 | **AI开发工具** 🚨 |
| 🌐 **[UNIVERSAL_AI_DEVELOPMENT_RULES.md](UNIVERSAL_AI_DEVELOPMENT_RULES.md)** | 通用规则 | 所有AI编程代理通用约束 | **AI开发工具** 🌐 |

### 开发指南.md 目录

```
1. 项目概述         - 功能模块、技术栈
2. 技术栈详解       - 核心依赖、开发工具
3. 开发环境搭建     - Python、Poetry、Playwright
4. 项目架构         - 目录结构、设计模式
5. 核心模块开发     - 配置、日志、数据库
6. GUI开发指南⭐    - UI/UX设计、样式管理、组件库
7. 自动化引擎       - 浏览器管理、反检测技术
8. 数据管理         - SQLAlchemy、数据仓库
9. 测试策略         - 单元测试、集成测试
10. 部署和打包      - PyInstaller打包
11. 开发最佳实践
12. 国际化支持
13. 常见问题
```

### GUI优化补充指南.md 目录

```
1. UI/UX设计原则    - 响应式设计、高DPI支持
2. 紧凑布局系统     - 多种密度级别
3. 完整组件库       - 模态框、表单、卡片
4. UI性能优化       - 虚拟滚动、延迟加载
5. 数据可视化       - 图表集成
6. 国际化支持       - i18n实现
```

### todos.md 目录

```
1. 第一阶段：项目基础架构    - 8个任务（2-3周）
2. 第二阶段：GUI开发        - 12个任务（3-4周）
3. 第三阶段：自动化引擎      - 10个任务（3-4周）
4. 第四阶段：数据管理        - 8个任务（2-3周）
5. 第五阶段：测试部署        - 7个任务（2-3周）
6. 开发里程碑                - 5个主要里程碑
7. 开发建议                  - 开发原则和风险控制
```

### FACTORY_AI_RULES.md 目录

```
1. 严格禁止行为      - 禁止精简版本、中途停止等
2. 必须执行行为      - 任务完成标准、进度管理要求
3. 任务执行流程      - 任务开始、执行、完成流程
4. 具体任务要求      - 5个核心任务的具体要求
5. 技术实现要求      - 代码完整性、错误处理等
6. 质量检查标准      - 代码质量、功能完整性检查
7. 违规处理          - 发现违规行为的处理方式
8. 标准回复模板      - 标准化的回复格式
```

### UNIVERSAL_AI_DEVELOPMENT_RULES.md 目录

```
1. 严格禁止行为      - 禁止精简版本、中途停止等通用约束
2. 必须执行行为      - 任务完成标准、进度管理要求
3. 任务执行流程      - 任务开始、执行、完成流程
4. 通用任务要求      - 5大类任务的具体要求
5. 技术实现要求      - 代码完整性、错误处理等
6. 质量检查标准      - 代码质量、功能完整性检查
7. 违规处理          - 发现违规行为的处理方式
8. 标准回复模板      - 标准化的回复格式
9. 最终目标          - 规则执行的目标和效果
10. 规则执行检查     - 任务前后的检查清单
```

---

## ⚠️ 重要警告

### Qt QSS ≠ CSS3 【必读】

> **如果你有 Web 前端经验，请先阅读**: [Qt_QSS_重要警告.md](Qt_QSS_重要警告.md)

Qt Style Sheets (QSS) 基于 **CSS2.1**，**不支持大部分 CSS3 特性**！

#### ❌ 不支持（不要使用）
```css
display: flex;            /* ❌ 无 flexbox */
transform: rotate(45deg); /* ❌ 无 transform */
transition: all 0.3s;     /* ❌ 无 transition */
animation: slide 1s;      /* ❌ 无 animation */
box-shadow: 0 2px 4px;    /* ❌ 无 box-shadow */
```

#### ✅ 正确方式
```python
# 布局 - 使用 Qt 布局管理器
layout = QHBoxLayout()

# 动画 - 使用 Qt 动画框架
anim = QPropertyAnimation(widget, b"geometry")

# 阴影 - 使用图形效果
shadow = QGraphicsDropShadowEffect()
```

**详细说明**: [Qt_QSS_重要警告.md](Qt_QSS_重要警告.md) ⚠️

---

## 🎨 UI设计核心

### 一句话记住

**标签透明,输入白色,强调黑色!**

### 组件底色

| 组件 | 底色 |
|-----|------|
| QLabel | 🔲 transparent |
| QLineEdit | ⬜ #FFFFFF |
| QPushButton.btn-primary | ⬛ #2C2C2C |
| QPushButton.btn-accent | 🔴 #0066FF |

### 三种主题

```
1. 纯黑白      - #000 + #FFF + 红
2. 柔和黑白⭐  - 深灰 + 浅灰 + 蓝
3. 高对比度    - 黑底白字 + 金黄
```

---

## 🧩 卡片组件

```python
from gui.components.card_components import *

# 指标卡片
MetricCard("CPU", "45%", trend="正常")

# 信息卡片
InfoCard("系统", "JDFlows v1.0", icon="ℹ️")

# 操作卡片
ActionCard("启动采集", "开始采集", "开始")

# 网格容器
grid = GridCardContainer(columns=3)
grid.add_card(card1)
```

---

## 📁 当前项目状态

### 现有文件
```
F:\jdflows_cs45\
├── 开发指南.md (60.3KB)              # 完整开发指南⭐
├── GUI优化补充指南.md (10.9KB)      # UI/UX高级组件
├── Qt_QSS_重要警告.md (必读)        # Qt QSS开发警告⚠️
├── todos.md (45个主要任务)          # 5阶段开发计划📋
├── AGENTS.md (AI代理)               # AI编程代理简报包🤖
├── FACTORY_AI_RULES.md (强制规则)   # Factory AI代理行为约束🚨
├── UNIVERSAL_AI_DEVELOPMENT_RULES.md (通用规则) # 所有AI编程代理通用约束🌐
└── README.md (本文件)               # 项目导航
```

### 规划的目录结构 (见开发指南.md 第4章)
```
jdflows/
├── src/
│   ├── core/              # 核心模块
│   ├── gui/               # GUI界面
│   │   ├── themes/        # 主题系统
│   │   └── components/    # 卡片组件
│   ├── automation/        # 自动化引擎
│   └── data/              # 数据管理
├── tests/                 # 测试代码
├── config/                # 配置文件
└── resources/             # 资源文件
```

> **注意**：目前项目处于**文档规划阶段**，代码实现请参考开发指南.md

---

## 💡 常见问题

**Q: 标签为什么要透明?**  
A: 保持极简风格,融入背景

**Q: 输入框可以透明吗?**  
A: 不行!需要白色底色明确边界

**Q: 如何切换主题?**  
```python
theme_manager = get_theme_manager()
theme_manager.switch_theme(ColorScheme.SOFT_BLACK_WHITE)
window.setStyleSheet(theme_manager.get_stylesheet())
```

---

## 📚 技术栈

```
Python 3.11+      PyQt6 6.6.0+
Playwright 1.40+  SQLAlchemy 2.0+
```

---

**详细内容**: [完整开发文档.md](完整开发文档.md) ⭐

**JDFlows Team** | MIT License
