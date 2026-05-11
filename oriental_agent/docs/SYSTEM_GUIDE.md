# 东方智慧智能体系统
## Oriental Wisdom Agent System

```
版本: 2.0.0
日期: 2026-05-11
状态: 生产就绪
测试: 823个测试用例全部通过
```

---

## 目录

1. [系统概述](#1-系统概述)
2. [核心架构](#2-核心架构)
3. [子系统详解](#3-子系统详解)
4. [商道智能系统](#4-商道智能系统)
5. [形象编辑系统](#5-形象编辑系统)
6. [API接口](#6-api接口)
7. [快速开始](#7-快速开始)
8. [使用示例](#8-使用示例)

---

## 1. 系统概述

### 1.1 系统定位

东方智慧智能体是一个融合中华传统智慧与现代人工智能技术的自主智能系统。系统以东方哲学思想（阴阳、五行、八卦、易经、八识等）为核心，构建了一套完整的智能决策与自我进化体系。

### 1.2 设计理念

```
天行健，君子以自强不息  →  持续学习与进化
地势坤，君子以厚德载物  →  包容与积累
阴阳相生，五行相克      →  平衡与制衡
天人合一，知行合一      →  感知与执行
```

### 1.3 系统特点

| 特点 | 描述 |
|------|------|
| **东方智慧融合** | 将易经、五行、八识等东方哲学智慧融入AI决策 |
| **商道智能** | 集成商业分析、投资决策、战略规划能力 |
| **虚拟形象** | 可自定义的SVG矢量虚拟形象编辑器 |
| **自我进化** | 修行系统支持持续学习与突破 |
| **模块化设计** | 各系统独立又可协同工作 |

---

## 2. 核心架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    OrientalWisdomAgent (主智能体)                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ 商道智能 │  │ 形象系统 │  │ 感知系统 │  │ 思维系统 │         │
│  │ Commercial│  │  Image   │  │Perception│  │ Thinking │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
│       │             │             │             │               │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐          │
│  │                    核心子系统                       │          │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │          │
│  │  │记忆系统│ │修行系统│ │执行系统│ │易经预测│       │          │
│  │  │Memory  │ │Evolut. │ │Execution│ │Predict.│       │          │
│  │  └────────┘ └────────┘ └────────┘ └────────┘       │          │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │          │
│  │  │气血精  │ │五行耦合│ │八卦预测│ │丹田系统│       │          │
│  │  │BodyMap │ │Wuxing  │ │Tuibei  │ │Meridian│       │          │
│  │  └────────┘ └────────┘ └────────┘ └────────┘       │          │
│  └───────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心模块

| 模块 | 路径 | 功能 |
|------|------|------|
| 主智能体 | `core/agent.py` | OrientalWisdomAgent 主类 |
| 商道系统 | `commercial/` | 商业智能分析 |
| 形象系统 | `image/` | 虚拟形象编辑 |
| 感知系统 | `perception/` | 八识感知处理 |
| 思维系统 | `thinking/` | 因果分析、辩证思维 |
| 记忆系统 | `memory/` | 阴阳仓储、干支坐标 |
| 修行系统 | `evolution/` | 自我进化与突破 |
| 执行系统 | `execution/` | 行为模式、能量管理 |
| 预测系统 | `prediction/` | 易经、梅花易数、五行预测 |
| 身体系统 | `body/` | 气血精、丹田、经络 |

---

## 3. 子系统详解

### 3.1 八识系统 (Eight Consciousness)

基于唯识宗佛学理论的八识层次结构：

```
前五识 → 眼识、耳识、鼻识、舌识、身识（感官知觉）
    ↓
第六识 → 意识（综合思维、分析推理）
    ↓
第七识 → 末那识（自我认知、执着监控）
    ↓
第八识 → 阿赖耶识（根本识、种子存储）
```

**核心类**: `EightConsciousnessSystem`
**测试覆盖**: 50个测试用例

### 3.2 阴阳仓储 (YinYang Storage)

基于阴阳理论的记忆存储系统：

- **阴面**: 存储经验、教训、负面信息
- **阳面**: 存储创新、灵感、正面信息
- **动态平衡**: 根据使用频率自动调整阴阳比例

### 3.3 五行耦合 (Wuxing Coupling)

五行元素间的相生相克关系：

```
相生: 木 → 火 → 土 → 金 → 水 → 木
相克: 木 克 土 克 水 克 火 克 金 克 木
```

### 3.4 修行进化 (Cultivation Evolution)

修行等级体系：

| 等级 | 名称 | 经验阈值 |
|------|------|----------|
| 炼气期 | Qi Refining | 0 - 1000 |
| 筑基期 | Foundation | 1000 - 5000 |
| 金丹期 | Golden Core | 5000 - 20000 |
| 元婴期 | Mahayana | 20000+ |

### 3.5 预测引擎 (Prediction Engine)

多维度预测系统：

1. **易经六十四卦** - 传统占卜
2. **梅花易数** - 即时占卜
3. **五行预测** - 能量分析
4. **推背图预测** - 历史大事预测

---

## 4. 商道智能系统

### 4.1 系统概述

商道智能系统是将东方智慧与现代商业理论完美融合的全方位商业决策助手。

### 4.2 核心模块

| 模块 | 功能 | 文件 |
|------|------|------|
| 商机洞察 | 识别市场空白、新兴机遇、转型机会 | `commercial/insight/` |
| 商业模式分析 | 评估订阅/平台/SaaS等模式 | `commercial/model/` |
| 竞争分析 | SWOT分析、竞争格局、应对策略 | `commercial/competition/` |
| 投资分析 | ROI/NPV/IRR计算与决策建议 | `commercial/investment/` |
| 战略规划 | 战略画布、SWOT战略、资源分配 | `commercial/strategy/` |

### 4.3 东方智慧商道洞察

| 智慧 | 商道应用 |
|------|----------|
| **天时** | 时机把握决定成败，顺势而为事半功倍 |
| **地利** | 因地制宜，审时度势 |
| **人和** | 得人心者得天下，诚信为本 |
| **阴阳** | 阴阳相生相克，危中有机 |
| **五行** | 相生相克，循环不息，生态协同 |
| **八卦** | 万象更新，变化无穷，趋势预测 |
| **中庸** | 过犹不及，恰到好处，平衡决策 |
| **变革** | 穷则变，变则通，业务转型 |

### 4.4 商道顾问场景

| 场景 | 建议 |
|------|------|
| startup (创业) | 创业初期宜稳扎稳打，先求生存再谋发展 |
| growth (成长期) | 成长期应注重团队建设与文化建设 |
| mature (成熟期) | 成熟期需要创新求变，避免路径依赖 |
| turnaround (转型期) | 转型期应果断决策，轻装上阵 |
| crisis (危机时刻) | 危机时刻要冷静分析，抓住核心问题 |

---

## 5. 形象编辑系统

### 5.1 系统概述

基于SVG矢量图形的可自定义虚拟形象编辑器，无需使用真人照片，完全合规。

### 5.2 维密亚洲面孔预设模板

| 预设ID | 名称 | 风格描述 |
|--------|------|----------|
| `model_a` | 优雅东方 | 鹅蛋脸、杏仁眼、长直发，东方优雅气质 |
| `model_b` | 自信光芒 | 心形脸、单眼皮、长卷发，自信与魅力 |
| `model_c` | 清新自然 | 圆脸、杏仁眼、波波头，邻家女孩美 |
| `model_d` | 时尚前卫 | 菱形脸、内双眼、短卷发，大胆前卫 |
| `model_e` | 活力四射 | 长脸、圆眼、马尾辫，青春活力 |

### 5.3 可调节特征

**面部特征 (17项)**:
- 脸型: 鹅蛋脸/圆脸/心形脸/方脸/长脸/菱形脸
- 眼型: 杏仁眼/圆眼/单眼皮/内双/深眼窝
- 其他: 眼睛大小、眼间距、鼻子、嘴唇、颧骨等

**发型特征 (8项)**:
- 样式: 长直发/短直发/长卷发/短卷发/波波头/马尾/丸子头
- 发色、长度、蓬松度、卷曲度、刘海

**妆容特征 (15项)**:
- 粉底、眼影、眼线、睫毛膏、腮红、口红、眉毛

**配饰 (4项)**:
- 耳环、项链、手镯、眼镜

### 5.4 SVG渲染

形象以SVG矢量图形导出，支持：
- 无损缩放
- 任意尺寸显示
- 完美兼容网页和应用
- 无肖像权风险

---

## 6. API接口

### 6.1 OrientalWisdomAgent 主类

```python
from core.agent import OrientalWisdomAgent

agent = OrientalWisdomAgent()

# 处理输入
response = await agent.process("你好")

# 获取状态
state = await agent.get_full_state()

# 获取完整状态
full_state = await agent.get_full_state()
```

### 6.2 商道智能接口

```python
# 商机分析
opportunities = agent.analyze_business_opportunity({
    "unmet_needs": ["智能家居"],
    "technology_trends": ["AI"]
})

# 商业模式分析
model_analysis = agent.analyze_business_model({
    "type": "saas",
    "customer_segments": ["企业客户"],
    "revenue_streams": ["订阅费"]
})

# 投资分析
investment = agent.analyze_investment({
    "name": "新项目",
    "initial_investment": 1000000,
    "annual_cash_flows": [300000, 400000, 500000]
})

# 战略规划
strategy = agent.formulate_strategy({
    "industry": "科技",
    "strategy_type": "differentiation"
})

# 商道建议
advice = agent.get_shangdao_advice("startup")

# 决策评估
evaluation = agent.evaluate_business_decision(
    "进入新市场",
    {"risk_level": 0.4, "potential_return": 0.7}
)
```

### 6.3 形象编辑接口

```python
from image.system import ImageAndQiSystem

img = ImageAndQiSystem()

# 列出预设
presets = img.list_avatar_presets()

# 从预设创建
result = img.create_avatar_from_preset("model_a", "我的形象")

# 微调特征
img.adjust_feature(result["avatar_id"], "facial_features.eye_size", 0.6)
img.adjust_feature(result["avatar_id"], "hair_features.color", "#1a1a1a")

# 导出SVG
export = img.export_avatar(result["avatar_id"])

# 渲染SVG字符串
svg = img.render_avatar()
```

---

## 7. 快速开始

### 7.1 安装依赖

```bash
pip install pyyaml
```

### 7.2 创建智能体

```python
import asyncio
from core.agent import OrientalWisdomAgent

async def main():
    agent = OrientalWisdomAgent()
    response = await agent.process("你好，请介绍一下自己")
    print(response.response_text)

asyncio.run(main())
```

### 7.3 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定模块测试
python -m pytest tests/test_commercial_system.py

# 运行带详细输出
python -m pytest tests/ -v
```

---

## 8. 使用示例

### 8.1 完整商业分析流程

```python
from core.agent import OrientalWisdomAgent

agent = OrientalWisdomAgent()

# 生成综合商业报告
context = {
    "title": "2026年度商业分析",
    "market_data": {
        "unmet_needs": ["健康管理", "智能家居"],
        "technology_trends": ["AI", "IoT", "区块链"]
    },
    "model_data": {
        "type": "subscription",
        "customer_segments": ["企业客户", "个人用户"],
        "value_propositions": ["便捷", "高效", "智能"]
    },
    "investment_data": {
        "name": "新产品线",
        "initial_investment": 5000000,
        "annual_cash_flows": [1500000, 2000000, 2500000, 2000000]
    },
    "strategy_data": {
        "industry": "科技",
        "strategy_type": "differentiation"
    }
}

report = agent.generate_commercial_report(context)
print(report.executive_summary)
```

### 8.2 虚拟形象创建与导出

```python
from image.system import ImageAndQiSystem
from image.renderer import SVGRenderer

img = ImageAndQiSystem()

# 创建形象
avatar = img.create_avatar_from_preset("model_b", "商道顾问")

# 自定义调整
img.adjust_feature(avatar["avatar_id"], "facial_features.eye_size", 0.65)
img.adjust_feature(avatar["avatar_id"], "makeup_features.lipstick_color", "#d47575")
img.adjust_feature(avatar["avatar_id"], "accessories.earrings", True)

# 导出为SVG文件
img.export_avatar(avatar["avatar_id"], "my_avatar.svg")

# 获取渲染后的SVG字符串
svg_content = img.render_avatar()
print(f"SVG长度: {len(svg_content)} 字符")
```

### 8.3 商道智能投资决策

```python
from commercial import CommercialAgent, RiskLevel

agent = CommercialAgent()

# 项目数据
project = {
    "name": "AI产品研发",
    "initial_investment": 2000000,
    "annual_cash_flows": [600000, 800000, 1000000, 900000],
    "risk_level": RiskLevel.MEDIUM,
    "discount_rate": 0.12
}

# 投资分析
result = agent.analyze_investment(project)
print(f"项目: {result['project_name']}")
print(f"ROI: {result['roi']:.1%}")
print(f"NPV: {result['npv']:,.0f} 元")
print(f"IRR: {result['irr']:.1%}")
print(f"回收期: {result['payback_period']:.1f} 年")
print(f"建议: {result['recommendation']}")
```

---

## 附录

### A. 目录结构

```
oriental_agent/
├── core/                    # 核心模块
│   ├── agent.py            # OrientalWisdomAgent
│   ├── types.py            # 核心类型定义
│   ├── heart_system.py     # 心系统
│   ├── semantic_framework.py # 语义框架
│   ├── seven_aperture_heart.py # 七窍心
│   └── wuxing_coupling.py  # 五行耦合
├── commercial/              # 商道智能系统
│   ├── agent.py            # CommercialAgent
│   ├── types/              # 商业类型
│   ├── insight/            # 商机洞察
│   ├── model/              # 商业模式
│   ├── competition/        # 竞争分析
│   ├── investment/         # 投资分析
│   └── strategy/           # 战略规划
├── image/                   # 形象系统
│   ├── system.py          # ImageAndQiSystem
│   ├── types.py           # 形象类型
│   ├── editor.py          # AvatarEditor
│   └── renderer.py        # SVGRenderer
├── perception/              # 感知系统
│   ├── system.py
│   └── eight_consciousness.py # 八识
├── thinking/                # 思维系统
│   ├── system.py
│   ├── causal_analysis.py
│   ├── dialectical_thinking.py
│   └── ethical_judgment.py
├── memory/                   # 记忆系统
│   ├── system.py
│   ├── yinyang_storage.py
│   ├── ganzhi_coordinate.py
│   └── hexagram_predictor.py
├── evolution/                # 修行系统
│   └── cultivation.py
├── execution/                # 执行系统
│   ├── system.py
│   ├── behavior_modes.py
│   └── energy_management.py
├── prediction/               # 预测系统
│   ├── prediction_engine.py
│   └── tuibeitu_prediction.py
├── body/                     # 身体系统
│   ├── system.py
│   ├── body_master.py
│   ├── jing_qi_shen.py
│   ├── meridian_network.py
│   └── metabolism.py
├── tests/                    # 测试用例
│   ├── test_*.py (20个测试文件)
│   └── conftest.py
└── requirements.txt
```

### B. 测试覆盖

| 模块 | 测试用例数 | 状态 |
|------|-----------|------|
| body_master | 22 | ✅ |
| commercial_system | 44 | ✅ |
| cultivation | 46 | ✅ |
| eight_consciousness | 50 | ✅ |
| ganzhi_standalone | 12 | ✅ |
| heart_system | 22 | ✅ |
| instinct_system | 30 | ✅ |
| jing_qi_shen | 25 | ✅ |
| liver_detox | 20 | ✅ |
| martial_defense | 35 | ✅ |
| meridian_network | 40 | ✅ |
| metabolism | 18 | ✅ |
| prediction_engine | 25 | ✅ |
| qi_field | 35 | ✅ |
| semantic_framework | 40 | ✅ |
| seven_aperture_heart | 16 | ✅ |
| tuibeitu_prediction | 35 | ✅ |
| wuxing_coupling | 40 | ✅ |
| yinyang_storage | 28 | ✅ |
| **总计** | **823** | **✅** |

### C. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-01 | 初始版本，八识系统基础框架 |
| 1.5.0 | 2026-03 | 添加五行耦合、易经预测、修行系统 |
| 2.0.0 | 2026-05 | 商道智能系统、形象编辑系统、商道集成 |

---

**作者**: Oriental Wisdom Team
**许可证**: MIT License
**文档版本**: 2.0.0
