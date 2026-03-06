---
name: ppt-visual-design
description: 为技术汇报PPT设计视觉方案并生成PPTX文件。当用户提到"PPT设计"、"幻灯片"、"汇报材料"、"技术演示"或需要为项目创建演示文稿时使用此技能。
---

# PPT 视觉设计与生成技能

为军工/技术项目汇报PPT提供完整的设计与生成方案。

## 核心能力

1. **配色方案设计**：根据项目类型推荐专业配色
2. **Gemini图片生成**：生成带中文标注的流程图、架构图、概念图
3. **python-pptx自动生成**：直接生成可编辑的PPTX文件

## 工作流程

### 第一步：需求分析

确认以下信息：
1. **项目类型**：海军/陆军/空军/AI智能体/通用技术
2. **汇报对象**：领导/专家/技术人员/混合
3. **使用场景**：现场汇报 / 发送阅读 / 两者兼顾
4. **PPT大纲**：章节结构和预计页数
5. **配色偏好**：简约现代/科技未来/传统正式

### 第二步：生成详细文案

基于源文档（技术方案/研究报告等），生成包含以下内容的详细文案文档：
- 每页标题、核心观点、支撑要点
- 视觉设计说明（布局、图表类型、配图需求）
- 演讲备注

**内容质量要求**：
- 文字不能是纯概括性表述，需要包含具体内容
- 详略得当：关键信息具体展开，次要信息简洁带过
- 单页文字控制在50字以内，但要有实质内容

文件命名：`[项目名]_PPT详细文案.md`

### 第三步：内容结构评审（生成PPT之前）

**目标**：在生成PPT之前，确保内容组织合理、逻辑连贯、信息密度适中。

**评审对象**：详细文案文档（不需要截图）

**评审Prompt**（Claude自身执行，详见 `structure_review_prompt.md`）：

#### 严重问题（阻断性，必须修改才能进入下一步）

| 问题类型 | 判定标准 |
|---------|---------|
| 完全重复 | 两页核心内容完全相同 |
| 逻辑断裂 | 相邻页面主题跳跃，缺少过渡 |
| 信息严重过载 | 单页正文文字>100字 |
| 主题混乱 | 一页包含2个以上不相关主题 |

#### 优化建议（非阻断，仅记录不强制修改）

| 建议类型 | 判定标准 |
|---------|---------|
| 部分重复 | 不同页面提到相同数据或案例 |
| 信息略多 | 单页正文文字60-80字 |
| 内容略概括 | 关键页面缺少具体数据支撑 |
| 信息密度不均 | 某些页面过于简单（<20字） |

#### 评审输出格式

```json
{
  "评审结果": "通过/不通过",
  "严重问题数量": 0,
  "严重问题列表": [
    {
      "问题类型": "完全重复",
      "涉及页码": [2, 10],
      "问题描述": "具体说明",
      "修改指令": {
        "操作": "replace/delete/merge",
        "页码": 2,
        "查找文本": "文案中的原文（精确匹配）",
        "替换文本": "完整的新内容"
      }
    }
  ],
  "优化建议列表": [
    {
      "建议类型": "内容略概括",
      "涉及页码": [8],
      "建议描述": "具体说明"
    }
  ]
}
```

#### 执行流程

1. 读取文案文档，按上述标准评审
2. 输出JSON格式的评审结果
3. **如果不通过**：立即执行所有严重问题的修改指令，修改文案文档，然后重新评审
4. **如果通过**：输出优化建议（仅供参考），直接进入第四步
5. **最多迭代2次**，2次后仍不通过则提示用户介入

**关键原则**：结构问题必须在生成PPT之前解决，否则后续修改成本极高。

#### 评审权限

**评审是执行者，不是咨询顾问**：
- 发现问题后立即修改，无需征求用户同意
- 可修改范围：文案文字、页面结构、信息组织
- 修改后自动进入下一轮评审，直到通过标准



### 第四步：Gemini图片生成

根据文案中的配图需求，使用Gemini生成图片。

#### 关键原则：图片类型决策

**需要中文文字标注的图片**（必须在prompt中要求中文标注）：
- 流程图（节点需要文字说明）
- 架构图（模块需要名称）
- 时间轴（阶段需要标注）
- 对比图（维度需要标签）
- 分层图（层级需要说明）

**可以纯图标的图片**（可以用"NO TEXT"）：
- 抽象概念图（AI神经网络、云计算等）
- 隐喻图（天平、齿轮、桥梁等）
- 装饰性背景图

#### Gemini提示词模板

**流程图/架构图（需要中文）**：
```
[图表类型] with [节点数量] nodes/phases, labeled in Chinese: "[节点1中文]", "[节点2中文]", ...,
arrows showing flow/connections,
professional business presentation style,
[主色] and [辅色] color scheme,
clean white background
```

**抽象概念图（纯图标）**：
```
Abstract [概念] illustration,
professional minimalist style,
[主色] and [辅色] color scheme,
NO TEXT,
clean white background,
business presentation style
```

**关键要素**：
- `clean white background` - 确保易于集成到PPT
- 指定配色方案（如 `dark blue (#1E3A8A) and orange (#F97316)`）
- `professional business presentation style` - 保持专业风格
- `16:9` 宽高比

#### 生成与验证流程

1. 调用 `mcp__gemini-image__generate_image()` 生成图片
2. 预览生成的图片
3. 如果文字标注不清晰或缺失，调整prompt重新生成
4. 记录图片文件路径（`e:\CC\cc-tools\tools\generated_images\gemini_*.jpg`）

### 第五步：编写python-pptx生成脚本

在项目目录创建 `gen_[项目名]_ppt.py` 脚本。

#### 方式一：使用模板库（推荐）

模板库提供三大风格（极简/商务/创意）× 3种配色变体 = 9种预设方案。

**导入模板**：
```python
import sys
sys.path.append('e:\CC\.claude\skills\ppt-visual-design')

from pptx import Presentation
from pptx.util import Inches
from templates import minimalist, corporate, creative
```

**选择风格**：
- 技术方案/商务汇报 → `minimalist` (极简风格)
- 数据报告/公司汇报 → `corporate` (商务风格)
- 品牌发布/创意提案 → `creative` (创意风格)

**使用示例**：
```python
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 极简风格封面
minimalist.minimalist_cover(
    prs,
    title="项目标题",
    subtitle="副标题",
    footer="公司名称
2026年3月",
    variant="business"  # business/tech/academic
)

# 极简风格图片页
minimalist.minimalist_image_center(
    prs,
    title="页面标题",
    image_path="path/to/image.jpg",
    caption="图片说明",
    variant="business"
)

prs.save("output.pptx")
```

详细文档见：`.claude/skills/ppt-visual-design/templates/README.md`

#### 方式二：自定义脚本（灵活）



#### 脚本结构模板

```python
# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

# 配色方案
COLOR_DARK_BLUE = RGBColor(30, 58, 138)  # 主色
COLOR_ORANGE = RGBColor(249, 115, 22)    # 辅色
COLOR_WHITE = RGBColor(255, 255, 255)
FONT_NAME = "Microsoft YaHei"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    return prs

def add_slide_with_image(prs, title, image_path, description):
    """带图片的标准页面"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 白色背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0,
                                prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_WHITE
    bg.line.fill.background()

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5),
                                         Inches(9), Inches(0.8))
    tf = title_box.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(32)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = COLOR_DARK_BLUE
    tf.paragraphs[0].font.name = FONT_NAME

    # 添加图片（居中）
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(2), Inches(1.8),
                                width=Inches(6))

    # 底部说明
    desc_box = slide.shapes.add_textbox(Inches(1), Inches(6),
                                       Inches(8), Inches(1))
    df = desc_box.text_frame
    df.text = description
    df.paragraphs[0].alignment = PP_ALIGN.CENTER
    df.paragraphs[0].font.size = Pt(18)
    df.paragraphs[0].font.color.rgb = COLOR_ORANGE
    df.paragraphs[0].font.name = FONT_NAME

def main():
    prs = create_presentation()

    # 逐页添加内容
    add_slide_with_image(prs, "标题", "图片路径", "说明文字")

    # 保存
    output_path = r"e:\CC\项目\[项目名]\[文件名].pptx"
    prs.save(output_path)
    print(f"PPT已生成：{output_path}")

if __name__ == "__main__":
    main()
```

#### 常用页面类型函数

**封面页**：标题 + 副标题 + 提案方信息
**内容页**：标题 + 文字要点
**图片页**：标题 + 图片 + 说明
**表格页**：标题 + 表格数据
**对比页**：标题 + 左右对比内容

### 第六步：生成并验证PPT

1. 运行脚本：`python gen_[项目名]_ppt.py`
2. 打开生成的PPTX文件验证
3. 根据反馈调整脚本或重新生成图片
4. 如遇文件占用错误，修改输出文件名（如添加版本号）

### 第七步：迭代优化（可选）

**触发条件**：用户说"请评审这个PPT"或"优化这个PPT"

**直接使用 `ppt-review-iterate` skill**：

```
用户："生成PPT后评审一下"
Claude：
1. 使用本 skill 生成初版 PPT（已包含第三步的内容结构评审）
2. 切换到 ppt-review-iterate skill
3. 自动导出截图（ppt_to_images.py）
4. 视觉评审 → 修改脚本 → v2.pptx
5. 如需继续优化 → 再次视觉评审 → v3.pptx
6. 完成
```

详细流程见 `ppt-review-iterate` skill 文档。

**视觉评审权限**：
- 可直接重新生成图片（调整 Gemini prompt）
- 可修改生成脚本（布局、配色、字体）
- 可调整图片风格和配色方案
- 修改后自动生成新版本 PPT，继续迭代



## 常见问题与解决方案

### 问题1：Gemini生成的图片没有文字标注

**原因**：prompt中使用了"NO TEXT"或未明确要求中文标注

**解决**：
- 流程图/架构图必须在prompt中列出所有节点的中文标注
- 示例：`labeled in Chinese: "第一阶段", "第二阶段", "第三阶段"`

### 问题2：图片背景色与PPT不协调

**原因**：未指定白色背景

**解决**：
- 在prompt中添加 `clean white background`
- 避免使用 `transparent background`（Gemini不支持透明背景）

### 问题3：生成PPT时报Permission Denied错误

**原因**：目标文件正在被PowerPoint打开

**解决**：
- 修改输出文件名（如添加 `_v2` 后缀）
- 或关闭已打开的PPT文件

### 问题4：中文字体显示异常

**原因**：系统缺少指定字体

**解决**：
- 使用 `Microsoft YaHei`（Windows系统自带）
- 或使用 `SimHei`（黑体）作为备选

## 输出文件组织

```
e:\CC\项目\[项目名]\
├── [项目名]_PPT详细文案.md          # 第二步输出
├── gen_[项目名]_ppt.py              # 第四步输出
└── [项目名]_方案.pptx               # 第五步输出
```

Gemini生成的图片统一保存在：
```
e:\CC\cc-tools\tools\generated_images\
└── gemini_*.jpg
```

## 最佳实践

1. **先文案后脚本**：详细文案是脚本编写的蓝图
2. **图片分类生成**：先生成需要文字的图，再生成纯图标的图
3. **迭代优化**：Gemini图片不满意时立即重新生成，不要将就
4. **保持简洁**：每页一个核心观点，避免信息过载
5. **配色一致**：所有Gemini图片使用相同的配色方案
6. **详略得当**：文字不能纯概括，关键页面要有具体数据/案例/对比；次要页面简洁带过

## Skill进化机制

本skill通过用户的语言描述和评价持续进化。

**触发方式**：用户在使用过程中的任何反馈，例如：
- "这次评审太严格了"→ 调整评审阈值
- "XX不应该算重复"→ 修正重复判定规则
- "配色不对，要正常点"→ 更新默认配色偏好
- "文字不能纯概括"→ 增加内容具体性要求

**Claude执行**：
1. 理解用户反馈的本质意图
2. 更新 `knowledge_base.md`（记录反馈和改进）
3. 如涉及核心流程变更，同步更新 `skill.md` 或 `structure_review_prompt.md`
4. 下次执行时自动读取并应用最新标准

**知识库位置**：`.claude/skills/ppt-visual-design/knowledge_base.md`
