# 技术文档写作流程

## 一、完整流程概览

```
需求输入 → 文档解读 → 大纲确认 → MD 起草 → 内容迭代 → 架构图 → Word 生成 → 格式调整
```

---

## Step 1 — 需求输入

- 接收原始任务书 / 合同 / 招标文件（PDF / Word）
- 若为 PDF，用 `mcp__doc-reader__read_pdf` 或 Read 工具读取全文
- 若为 Word，用 `mcp__doc-reader__read_word` 读取

---

## Step 2 — 文档解读

- 完整读取原始文件，提炼以下要素：
  - 核心需求（需要做什么）
  - 技术指标（含数量，如"10项指标"、"支持≥3种"）
  - 交付物清单（报告几份、系统几套、文档几份）
  - 约束条件（合同金额、禁用词、保密要求等）
- 输出"需求摘要"给用户确认，确保不遗漏关键指标

---

## Step 3 — 大纲确认

- 按"背景→需求→方案→关键技术→指标→成果"结构列出章节大纲
- **等待用户明确确认后再展开正文，不擅自跳过此步**
- 大纲一旦确认，后续不随意增删章节

---

## Step 4 — MD 起草

- 以 `.md` 文件作为内容唯一权威源（source of truth）
- 逐章生成，每章完成后等用户确认再继续
- 写作原则：
  - 工作描述（做什么工程工作）而非效果承诺（保证什么结果）
  - 只写刚好覆盖指标要求的内容，不承诺额外功能
  - 展示型内容（表格、分类框架）可放心写，研究性工作承诺需谨慎

---

## Step 5 — 内容迭代

- 用户反馈 → 直接修改 `.md` 文件对应段落
- **同步更新 `gen_docx.py` 中对应的硬编码内容**（两者必须保持一致）
- 常见修改类型：
  - 段落改写：Edit 工具定位 old_string → new_string
  - 章节新增：确定插入位置后在 MD 和 gen_docx.py 中同时添加
  - 章节删除：MD 和 gen_docx.py 中同时删除对应内容

---

## Step 6 — 架构图生成

- 脚本位置：`scripts/gen_arch_svg.py`
- 输出文件：`系统总体架构图.svg`
- 用 Visio「文件→打开」直接导入，文字/框/箭头完全可编辑
- 操作方式：每次重写前先 Read 脚本确认已读，再用 Write 工具覆盖
- SVG 规范：
  - 中文字体：`Microsoft YaHei, SimHei, sans-serif`
  - 箭头：用 `<marker>` 定义，不用图片
  - 尺寸：通常 900×750 至 900×900 px

---

## Step 7 — Word 生成

- 脚本位置：`scripts/gen_docx.py`
- 脚本性质：**硬编码**（非通用 MD 解析器），内容变更后需手动同步
- 输出文件：`样本生成项目技术规格书vX.X.docx`
- 运行命令：`python scripts/gen_docx.py`
- 常见问题：
  - `PermissionError`：目标文件被 Word 打开 → 改版本号（v0.1 → v0.2）再运行
  - 终端中文乱码：正常现象（Windows 代码页问题），文档内容不受影响

### gen_docx.py 常用函数

| 函数 | 用途 |
|------|------|
| `add_chapter_title(doc, text)` | 一级标题（一、二、三…） |
| `add_section_title(doc, text)` | 二级标题（4.1, 4.2…） |
| `add_subsection_title(doc, text)` | 三级标题（4.2.1…） |
| `add_subsubsection_title(doc, text)` | 四级标题（4.1.1…） |
| `add_body(doc, text)` | 正文段落 |
| `add_body_bold_prefix(doc, bold, normal)` | 正文含粗体前缀（如"**研究目标**：…"） |
| `add_bullet(doc, text, bold_prefix=None)` | 列表项（可带粗体前缀） |
| `add_formula(doc, latex_str)` | 独立公式块（LaTeX → OMML） |
| `add_body_md(doc, text)` | 含行内公式的正文（`$...$`） |
| `add_table(doc, headers, rows, col_widths)` | 表格 |

---

## Step 8 — 格式调整

### 行距
- 正文行距：`LINE_SPACING_BODY = 1.5`（文件顶部常量，改这里自动生效）
- 标题行距：`LINE_SPACING_HEADING = 1.5`
- 规则：float 值自动用 auto 规则（1.5倍行距）；`Pt(N)` 值用 EXACTLY 规则（封面等特殊段落）
- **注意**：`add_formula` / `add_body_md` / `add_bullet_md` 内部也需使用 `LINE_SPACING_BODY`，不能硬编码 `1.0`

### 其他格式常量（gen_docx.py 顶部）
| 常量 | 当前值 | 说明 |
|------|--------|------|
| `FONT_CN` | 仿宋_GB2312 | 中文字体 |
| `FONT_EN` | Calibri | 英文字体 |
| `FONT_TITLE` | 方正小标宋简体 | 封面大标题字体 |
| `FONT_SIZE_BODY` | Pt(14) | 正文字号 |
| `FIRST_INDENT` | Cm(0.74) | 首行缩进 |

---

## 二、关键文件结构（以海上无人集群项目为例）

```
海上无人集群/
├── 样本生成项目_技术规格书.md          ← 内容权威源
├── 系统总体架构图.svg                   ← 生成的矢量架构图
├── 样本生成项目技术规格书v0.2.docx      ← 最新 Word 交付文档
├── scripts/
│   ├── gen_docx.py                     ← Word 生成脚本
│   └── gen_arch_svg.py                 ← SVG 架构图生成脚本
└── archive/                            ← 历史版本归档
```

---

## 三、军工文档写作注意事项

- **术语规范**：全文统一，不混用（如"无人集群"不混"无人蜂群"）
- **仿真平台**：不写"UE"，统称"仿真平台"（国产化要求）
- **海空元素**：舰载机/无人机作为火力投送与侦察手段，不实现空中平台独立控制
- **不承诺效果**：写"支持XX功能"而非"实现XX效果"/"保证XX性能"
- **不增加工作量**：遇到"锦上添花"内容先列出给用户确认，不直接写入
