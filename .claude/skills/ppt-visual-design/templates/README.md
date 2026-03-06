# PPT 模板库使用指南

## 目录结构

```
templates/
├── __init__.py           # 模板库入口
├── color_schemes.py      # 配色方案（9种）
├── minimalist.py         # 极简风格模板
├── corporate.py          # 商务风格模板
└── creative.py           # 创意风格模板
```

## 快速开始

### 1. 导入模板

```python
import sys
sys.path.append('e:\\CC\\.claude\\skills\\ppt-visual-design')

from pptx import Presentation
from templates import minimalist, corporate, creative
from templates.color_schemes import get_scheme
```

### 2. 创建演示文稿

```python
from pptx.util import Inches

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)
```

### 3. 使用模板

#### 极简风格示例

```python
# 封面页
minimalist.minimalist_cover(
    prs,
    title="AI 技术方案",
    subtitle="面向企业的智能化解决方案",
    footer="超参数科技\\n2026年3月",
    variant="business"  # business/tech/academic
)

# 图片页
minimalist.minimalist_image_center(
    prs,
    title="核心技术架构",
    image_path="path/to/image.jpg",
    caption="基于深度学习的智能决策系统",
    variant="business"
)
```

#### 商务风格示例

```python
# 封面页
corporate.corporate_cover(
    prs,
    title="2026 年度业务报告",
    subtitle="数字化转型成果展示",
    company="超参数科技（深圳）有限公司",
    variant="conservative"  # conservative/modern/tech
)

# 数据页
corporate.corporate_data_slide(
    prs,
    title="关键业绩指标",
    data_points=[
        "营收增长 45%，达到 5000 万元",
        "客户数量突破 100 家",
        "产品线扩展至 3 个领域",
        "团队规模增长至 50 人"
    ],
    variant="conservative"
)
```

#### 创意风格示例

```python
# 暗黑封面
creative.creative_dark_cover(
    prs,
    title="未来已来",
    subtitle="AI 驱动的下一代产品",
    variant="neon"  # neon/gradient/retro
)

# 非对称布局
creative.creative_asymmetric(
    prs,
    title="创新突破",
    image_path="path/to/image.jpg",
    text="我们重新定义了行业标准，创造了全新的用户体验",
    variant="neon"
)
```

## 配色方案

### 极简风格（Minimalist）

| 变体 | 主色 | 强调色 | 适用场景 |
|------|------|--------|---------|
| business | 深灰 #2C3E50 | 商务蓝 #3498DB | 商务汇报 |
| tech | 深蓝 #1E3A8A | 橙色 #F97316 | 技术方案 |
| academic | 黑色 #000000 | 灰色 #6B7280 | 学术演讲 |

### 商务风格（Corporate）

| 变体 | 主色 | 强调色 | 适用场景 |
|------|------|--------|---------|
| conservative | 深蓝 | 灰色 | 保守型企业 |
| modern | 黑色 | 金色 | 现代企业 |
| tech | 深紫 | 青色 | 科技公司 |

### 创意风格（Creative）

| 变体 | 主色 | 强调色 | 适用场景 |
|------|------|--------|---------|
| neon | 黑底 | 荧光绿/粉 | 创意提案 |
| gradient | 靛蓝 | 粉红 | 品牌发布 |
| retro | 棕褐 | 黄色 | 复古主题 |

## 自定义配色

```python
from templates.color_schemes import get_scheme

# 获取配色方案
colors = get_scheme("minimalist", "business")

# 使用配色
colors["primary"]   # 主色
colors["accent"]    # 强调色
colors["white"]     # 白色
colors["light"]     # 浅色
```

## 最佳实践

1. **风格一致性**：同一 PPT 使用同一风格和变体
2. **配色协调**：使用预设配色方案，避免自定义颜色
3. **留白充足**：每页一个核心观点
4. **字体统一**：默认使用微软雅黑
5. **图片质量**：使用高清图片，宽度建议 5.5 英寸

## 扩展开发

### 添加新的页面模板

在对应风格文件中添加函数：

```python
def minimalist_new_layout(prs, title, content, variant="business"):
    colors = get_scheme("minimalist", variant)
    slide = create_minimalist_slide(prs, colors)
    # 添加布局逻辑
    pass
```

### 添加新的配色变体

在 `color_schemes.py` 中添加：

```python
MINIMALIST_SCHEMES["new_variant"] = {
    "primary": RGBColor(r, g, b),
    "accent": RGBColor(r, g, b),
    "white": RGBColor(255, 255, 255),
    "light": RGBColor(r, g, b),
}
```
