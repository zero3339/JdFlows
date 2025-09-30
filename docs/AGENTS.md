# JDFlows

京东商品采集系统，基于Python + PyQt6 + Playwright的极简黑白UI应用。

## Build & Test

- 安装依赖: `pip install -r requirements.txt`
- 安装浏览器: `playwright install chromium`
- 运行测试: `pytest`
- 代码检查: `black . && flake8 . && mypy .`
- 运行UI演示: `python demo_minimalist_ui.py`
- 运行主程序: `python main.py`

## Project Layout

```
jdflows/
├── src/
│   ├── core/              # 核心模块 (配置、日志、异常)
│   ├── gui/               # GUI界面
│   │   ├── themes/        # 主题系统
│   │   ├── components/    # 卡片组件库
│   │   └── pages/         # 页面组件
│   ├── automation/        # 自动化引擎
│   │   ├── browser/       # 浏览器管理
│   │   ├── stealth/       # 反检测技术
│   │   └── extractors/    # 数据提取器
│   └── data/              # 数据管理
│       ├── models/        # SQLAlchemy模型
│       ├── repositories/  # 数据仓库
│       └── cache/         # 缓存系统
├── tests/                 # 测试代码
├── config/                # 配置文件
├── resources/             # 资源文件
└── docs/                  # 项目文档
```

## Development Patterns & Constraints

### 代码风格
- Python 3.11+，使用类型注解
- 遵循PEP 8，100字符行限制
- 使用Black格式化，Flake8检查，mypy类型检查
- 异步编程使用qasync + asyncio
- GUI组件继承自Qt基类，使用QSS样式

### 架构约束
- 核心模块在`src/core/`，GUI在`src/gui/`
- 自动化引擎在`src/automation/`，数据管理在`src/data/`
- 使用单例模式管理配置、日志、样式管理器
- 组件通信使用信号槽机制和事件总线
- 数据库使用SQLAlchemy 2.0+，支持异步操作

### UI设计原则
- **极简黑白风格**: 标签透明，输入框白色，按钮黑色
- **三种主题**: 纯黑白、柔和黑白(推荐)、高对比度
- **响应式布局**: 支持移动端和桌面端适配
- **卡片组件**: MetricCard、InfoCard、ActionCard、ListCard、StatusCard

## Git Workflow Essentials

1. 从`main`分支创建功能分支: `feature/<功能名>` 或 `bugfix/<问题名>`
2. 提交前运行: `pytest && black . && flake8 . && mypy .`
3. 允许在功能分支上强制推送: `git push --force-with-lease`
4. 保持提交原子性: `feat: 添加新功能`, `fix: 修复问题`, `test: 添加测试`

## Evidence Required for Every PR

每个PR必须包含:
- 所有测试通过 (`pytest`)
- 代码格式和类型检查通过 (`black . && flake8 . && mypy .`)
- 修改范围限制在指定路径内
- **证明工件**:
  - 错误修复 → 先添加失败测试，现在通过
  - 新功能 → 新测试或视觉快照证明行为
- 一段话的提交/PR描述，说明意图和根本原因
- 无覆盖率下降，无未解释的运行时依赖

## Security

- API密钥存储在环境变量中
- 数据库连接使用连接池
- 敏感数据加密存储
- 反检测技术避免被识别为自动化

## External Services

- Playwright浏览器自动化
- SQLite数据库 (开发) / PostgreSQL (生产)
- 京东网站数据采集

## Gotchas

### Qt QSS限制
- **不支持CSS3特性**: 无flexbox、transform、transition、animation、box-shadow
- **正确方式**: 使用Qt布局管理器、QPropertyAnimation、QGraphicsEffect
- 详细说明见: `docs/Qt_QSS_重要警告.md`

### 异步编程
- GUI事件循环与asyncio集成使用qasync
- 数据库操作必须使用异步SQLAlchemy
- 浏览器操作使用Playwright异步API

### 反检测技术
- 使用playwright-stealth插件
- 随机化浏览器指纹
- 模拟人类行为模式
- 避免检测特征

## Conventions & Patterns

### 命名规范
- 类名使用PascalCase: `MetricCard`, `BrowserManager`
- 函数名使用snake_case: `get_theme_manager()`, `extract_product_info()`
- 常量使用UPPER_CASE: `DEFAULT_TIMEOUT`, `MAX_RETRIES`
- 私有方法前缀下划线: `_internal_method()`

### 文件组织
- 每个模块一个文件，功能单一
- 测试文件以`test_`开头
- 配置文件使用JSON格式
- 资源文件按类型分类存储

### 错误处理
- 使用自定义异常类: `JDFlowsError`, `BrowserError`, `DatabaseError`
- 全局异常处理器记录错误日志
- 用户友好的错误提示
- 优雅降级和恢复机制

## Architecture Overview

JDFlows采用分层架构:
- **表示层**: PyQt6 GUI组件和页面
- **业务层**: 控制器和业务逻辑
- **数据层**: SQLAlchemy模型和数据仓库
- **基础设施层**: 浏览器管理、反检测、缓存

数据流: GUI事件 → 控制器 → 业务逻辑 → 数据仓库 → 数据库
自动化流: 任务调度 → 浏览器管理 → 反检测 → 数据提取 → 数据存储

## 开发任务优先级

参考`docs/todos.md`中的45个主要任务:
1. **第一阶段**: 项目基础架构 (8个任务，2-3周)
2. **第二阶段**: GUI开发 (12个任务，3-4周)
3. **第三阶段**: 自动化引擎 (10个任务，3-4周)
4. **第四阶段**: 数据管理 (8个任务，2-3周)
5. **第五阶段**: 测试部署 (7个任务，2-3周)

按阶段顺序开发，确保核心功能优先完成。
