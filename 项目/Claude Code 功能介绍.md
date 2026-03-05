# Claude Code 功能完整介绍

> 本文档面向中文用户，系统介绍 Claude Code 的所有主要功能模块。
> 适用版本：Claude Code（claude.ai/code）最新版

---

## 目录

1. [基础文件操作](#1-基础文件操作)
2. [代码操作能力](#2-代码操作能力)
3. [命令行执行](#3-命令行执行)
4. [会话管理](#4-会话管理)
5. [多模型支持](#5-多模型支持)
6. [斜杠命令（Slash Commands）](#6-斜杠命令)
7. [快捷键](#7-快捷键)
8. [子代理 Task 工具](#8-子代理-task-工具)
9. [CLAUDE.md 配置文件](#9-claudemd-配置文件)
10. [MCP 服务器](#10-mcp-服务器)
11. [Hooks 钩子机制](#11-hooks-钩子机制)
12. [权限控制模式](#12-权限控制模式)
13. [Web 搜索与抓取](#13-web-搜索与抓取)
14. [Notebook 支持](#14-notebook-支持)
15. [技能（Skills）系统](#15-技能-skills-系统)
16. [记忆与上下文管理](#16-记忆与上下文管理)

---

## 1. 基础文件操作

### 是什么
Claude Code 内置了一套文件系统工具，可以直接读取、创建、编辑文件，而无需借助外部工具。

### 能做什么

| 工具 | 功能 |
|------|------|
| `Read` | 读取文件内容，支持 PDF、图片、Notebook 等多种格式 |
| `Write` | 创建或完整覆写文件 |
| `Edit` | 对文件进行精确的字符串替换，只发送差异部分 |
| `Glob` | 按 glob 模式搜索匹配的文件路径（如 `**/*.py`） |
| `Grep` | 在文件内容中按正则表达式搜索（基于 ripgrep） |

### 使用示例

```
# 读取文件
"读取 src/main.py 的内容"

# 搜索所有 TypeScript 文件
"找出项目中所有包含 TODO 的 .ts 文件"

# 精确编辑
"将函数 fetchData 的超时时间从 3000 改为 5000"
```

---

## 2. 代码操作能力

### 是什么
Claude Code 的核心能力，可以理解、生成、调试和重构代码，支持几乎所有主流编程语言。

### 能做什么

- **代码生成**：根据需求描述生成新函数、模块、类
- **Bug 修复**：定位错误原因，给出修复方案并直接修改代码
- **代码解释**：解读任意复杂的代码逻辑、算法原理
- **重构优化**：改善代码结构、消除重复、提升可读性
- **测试生成**：为现有代码自动生成单元测试
- **代码审查**：识别潜在问题、安全漏洞、性能瓶颈
- **类型标注**：为 Python/TypeScript 等语言添加类型注解
- **API 对接**：根据文档生成 API 调用代码

### 使用示例

```
"帮我写一个 FastAPI 接口，接收 POST 请求，将数据存入 SQLite"

"这段代码为什么会报 KeyError？怎么修复？"

"把这个 utils.py 重构成更模块化的结构"

"为 auth.py 中的所有公共函数写单元测试"
```

---

## 3. 命令行执行

### 是什么
Claude Code 可以通过 `Bash` 工具直接在用户系统上执行 Shell 命令，包括 Git、npm、pip、系统命令等。

### 能做什么

- 运行测试（`pytest`、`npm test`、`cargo test`等）
- 执行 Git 操作（`git status`、`git diff`、`git commit`等）
- 安装依赖（`pip install`、`npm install`等）
- 运行构建脚本
- 执行数据库迁移
- 查看进程、端口、系统状态
- 运行自定义脚本（Python、Shell 等）

### 使用示例

```
"运行测试，看看有哪些失败"

"帮我 git add 所有修改过的文件，然后提交"

"安装 pdfplumber 这个 Python 包"
```

> ⚠️ 高风险命令（如 `rm -rf`、`git push --force`）会在执行前请求用户确认。

---

## 4. 会话管理

### 是什么
Claude Code 提供多种会话级别的管理命令，用于控制上下文、模型、对话历史等。

### 核心命令

| 命令 | 作用 |
|------|------|
| `/clear` | 清空当前对话历史，重置上下文（保留 CLAUDE.md 配置） |
| `/model` | 切换当前使用的模型（Haiku / Sonnet / Opus） |
| `/help` | 查看所有可用命令和快捷键 |
| `/tasks` | 查看当前所有任务的状态 |
| `/fast` | 切换 Fast 模式（同一模型但更快输出） |
| `/memory` | 查看当前加载的记忆文件 |
| `/status` | 查看会话状态（模型、Token 用量等） |

### 上下文管理建议

```
# 典型工作流
1. 用 /clear 清空无关的上下文
2. 用 /model 切换到适合当前任务的模型
3. 执行任务
4. 完成后可再次 /clear 准备下一个任务
```

---

## 5. 多模型支持

### 是什么
Claude Code 支持多个 Claude 模型，可根据任务复杂度选择最合适的模型。

### 可用模型对比

| 模型 | 模型 ID | 特点 | 适用场景 |
|------|---------|------|---------|
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | 最快、成本最低 | 快速问答、简单查询、高频对话 |
| **Sonnet 4.6** | `claude-sonnet-4-6` | 均衡、默认模型 | 中等复杂分析、代码生成 |
| **Opus 4.6** | `claude-opus-4-6` | 最强、成本最高 | 复杂文档、战略决策、深度推理 |

### Extended Thinking（深度思考模式）

- 快捷键：`Alt + T`（切换开关）
- 效果：模型在回复前先进行深度推理，过程可见
- 适用：需要多步推理的复杂问题、架构设计、策略分析
- 注意：仅 Opus 和 Sonnet 支持此模式

### 切换方式

```
/model haiku    → 切换到 Haiku
/model sonnet   → 切换到 Sonnet（默认）
/model opus     → 切换到 Opus
Alt+T           → 开关 Extended Thinking
```

---

## 6. 斜杠命令

### 是什么
斜杠命令是用户可以直接在对话中调用的预定义工作流，也可以自定义。

### 内置斜杠命令

| 命令 | 功能 |
|------|------|
| `/commit` | 自动分析变更内容，生成符合规范的 Git 提交信息并提交 |
| `/review-pr` | 审查指定的 Pull Request，分析代码质量和潜在问题 |
| `/model` | 切换模型 |
| `/clear` | 清空上下文 |
| `/help` | 查看帮助 |

### 自定义斜杠命令（Skills）

用户可以在 `~/.claude/commands/` 或项目 `.claude/commands/` 目录下创建 `.md` 文件，定义自己的斜杠命令。

**示例**：创建 `/daily-report` 命令

```markdown
# .claude/commands/daily-report.md

请根据今天的 git log 和代码变更，自动生成一份日报：
1. 完成了什么
2. 遇到了什么问题
3. 明天计划做什么
```

调用方式：`/daily-report`

---

## 7. 快捷键

### 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Alt + T` | 切换 Extended Thinking（深度思考）模式 |
| `Ctrl + C` | 中断当前正在执行的操作 |
| `↑ / ↓` | 浏览历史输入记录 |
| `Ctrl + R` | 搜索历史命令（Shell 风格） |
| `Ctrl + L` | 清空终端显示（不清除上下文） |
| `Tab` | 自动补全命令和文件路径 |
| `Ctrl + D` | 退出 Claude Code |

### 自定义快捷键

可在 `~/.claude/keybindings.json` 中配置自定义快捷键：

```json
{
  "bindings": [
    {
      "key": "ctrl+shift+c",
      "command": "/commit"
    }
  ]
}
```

---

## 8. 子代理 Task 工具

### 是什么
Claude Code 可以通过 `Task` 工具启动专门化的子代理，用于处理需要独立执行的复杂子任务，或并行处理多个独立任务。

### 可用子代理类型

| 子代理类型 | 功能 | 适用场景 |
|-----------|------|---------|
| `general-purpose` | 通用代理，拥有所有工具 | 复杂的多步骤研究和执行任务 |
| `Explore` | 代码库探索专用 | 快速找文件、搜索关键词、理解代码结构 |
| `Plan` | 软件架构设计 | 设计实现方案、分析架构权衡 |
| `claude-code-guide` | Claude Code 使用指南 | 询问 Claude Code 功能、API 使用等 |
| `statusline-setup` | 状态栏配置 | 配置 Claude Code 状态行设置 |

### 并行执行能力

Task 工具支持多个子代理并行执行，显著提升效率：

```
# 示例：并行处理3个独立任务
- 子代理1：分析项目A的技术方案
- 子代理2：分析项目B的成本结构
- 子代理3：生成文档模板

→ 三者同时运行，而非顺序执行
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `subagent_type` | 子代理类型 |
| `model` | 使用的模型（haiku/sonnet/opus） |
| `run_in_background` | 是否后台执行（true/false） |
| `isolation: "worktree"` | 在独立的 git worktree 中运行，避免影响主分支 |
| `resume` | 通过 agentId 恢复上次中断的子代理 |

---

## 9. CLAUDE.md 配置文件

### 是什么
`CLAUDE.md` 是 Claude Code 的项目级配置文件，每次会话都会自动加载，用于持久化保存项目信息、偏好设置和工作规范。

### 查找顺序

Claude Code 会按以下顺序加载配置：
1. `~/.claude/CLAUDE.md`（全局用户级配置）
2. 当前工作目录的 `CLAUDE.md`（项目级配置）
3. 子目录中的 `CLAUDE.md`（局部覆盖）

### 常见配置内容

```markdown
# CLAUDE.md 示例

## 项目概述
这是一个 FastAPI 后端项目，使用 PostgreSQL 数据库。

## 开发规范
- 使用 Black 格式化 Python 代码
- 所有函数必须有类型标注
- 提交信息使用中文

## 常用命令
- 启动开发服务器：`uvicorn main:app --reload`
- 运行测试：`pytest tests/ -v`
- 代码格式化：`black . && isort .`

## 注意事项
- 不要直接修改 migrations/ 目录下的文件
- 环境变量在 .env 文件中，不要提交到 git
```

### 记忆文件系统

Claude Code 支持持久化记忆目录（`~/.claude/projects/<project>/memory/`），可通过 `MEMORY.md` 跨会话保留关键信息：

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 主记忆文件（自动加载）
├── architecture.md    # 架构记录
├── debugging.md       # 调试经验
└── patterns.md        # 代码模式
```

---

## 10. MCP 服务器

### 是什么
MCP（Model Context Protocol）是 Anthropic 的开放协议，允许 Claude Code 连接外部工具和服务，极大扩展其能力边界。

### 常见 MCP 用途

| 类别 | 示例 MCP | 功能 |
|------|---------|------|
| **数据库** | PostgreSQL MCP | 直接查询和修改数据库 |
| **浏览器** | Browser MCP | 控制浏览器，截图、填写表单 |
| **设计工具** | Figma MCP | 读取设计稿，直接生成代码 |
| **项目管理** | GitHub MCP | 读写 Issues、PR、Wiki |
| **通信** | Slack MCP | 发送消息、读取频道记录 |
| **文件存储** | Google Drive MCP | 读写云端文件 |

### 配置方式

在 `~/.claude/settings.json` 或项目 `.claude/settings.json` 中配置：

```json
{
  "mcpServers": {
    "my-database": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

---

## 11. Hooks 钩子机制

### 是什么
Hooks 是 Claude Code 在特定事件触发时自动执行的 Shell 命令，类似于 Git Hooks。

### 可用钩子类型

| 钩子 | 触发时机 |
|------|---------|
| `PreToolUse` | Claude 即将调用某个工具前 |
| `PostToolUse` | Claude 调用工具后 |
| `Notification` | 有新通知时（如长任务完成） |
| `Stop` | Claude 完成响应时 |

### 使用场景

```json
// .claude/settings.json 示例
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $TOOL_RESULT_FILE"
          }
        ]
      }
    ]
  }
}
```

**实际用途举例**：
- 每次文件编辑后自动运行代码格式化
- 每次 Bash 执行后自动记录日志
- 任务完成时发送桌面通知
- 文件修改后自动触发测试

---

## 12. 权限控制模式

### 是什么
Claude Code 提供多级权限控制，用于平衡操作效率与安全风险。

### 三种权限模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **默认模式** | 危险操作会弹出确认提示 | 日常开发（推荐） |
| **自动批准模式** | 指定工具/命令自动执行，无需确认 | 高频操作、CI/CD 环境 |
| **只读模式** | 只允许读取文件，禁止写入和执行 | 代码审查、不可信代码库 |

### 配置示例

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(git *)",         // 自动允许所有 git 命令
      "Bash(npm test)",      // 自动允许运行测试
      "Edit(**/*.md)"        // 自动允许编辑 Markdown
    ],
    "deny": [
      "Bash(rm -rf *)",      // 永远禁止递归删除
      "Bash(git push *)"     // 禁止 push（需手动操作）
    ]
  }
}
```

---

## 13. Web 搜索与抓取

### 是什么
Claude Code 内置网络访问能力，可以搜索互联网信息和抓取特定网页内容。

### 两种工具

**WebSearch（网页搜索）**
- 用途：搜索最新信息、技术文档、新闻事件
- 示例：`"搜索 React 19 新特性有哪些"`
- 特点：返回搜索结果摘要，含来源链接；**必须附带来源说明**

**WebFetch（网页抓取）**
- 用途：获取指定 URL 的完整内容并分析
- 示例：`"抓取这个 API 文档页面，整理出所有接口参数"`
- 特点：将 HTML 转为 Markdown，用小型模型处理
- 注意：需要提供完整 URL，Claude Code 不会猜测或生成 URL

### 限制

- 仅在美国地区可使用 WebSearch
- 不会主动生成或猜测 URL
- 部分网站有反爬限制

---

## 14. Notebook 支持

### 是什么
Claude Code 可以直接读取、编辑 Jupyter Notebook（`.ipynb`）文件，查看代码和输出，并修改特定单元格。

### 能做什么

- **读取**：`Read` 工具直接读取 `.ipynb`，显示所有 Cell 的代码、输出和可视化
- **编辑单元格**：`NotebookEdit` 工具可替换、插入、删除指定 Cell
- **运行分析**：理解 Notebook 中的数据分析逻辑，提出改进建议
- **代码补全**：在 Notebook 中添加新的分析步骤

### 使用示例

```
"读取 analysis.ipynb，解释第3个Cell在做什么"

"在 data_processing.ipynb 的第5个Cell后面，插入一个新的Cell，
用 seaborn 画出数据的分布图"
```

---

## 15. 技能（Skills）系统

### 是什么
Skills 是用户自定义的可复用工作流，通过 `.md` 文件定义，以斜杠命令的形式调用。

### 文件位置

```
~/.claude/commands/          # 全局 Skills（所有项目可用）
.claude/commands/            # 项目级 Skills（仅当前项目可用）
```

### 创建示例

```markdown
# .claude/commands/write-doc.md
# 使用方式：/write-doc [文件名]

请为 $ARGUMENTS 这个文件：
1. 阅读其源代码
2. 分析其功能和参数
3. 生成对应的中文技术文档
4. 保存为 docs/$ARGUMENTS.md
```

### 调用方式

```
/write-doc utils.py
```

---

## 16. 记忆与上下文管理

### 是什么
Claude Code 提供两种记忆机制：会话内上下文（临时）和跨会话记忆（持久化）。

### 会话内上下文

- **容量**：当前对话中的所有消息，直到 `/clear`
- **压缩**：接近上下文限制时自动压缩历史消息
- **管理**：用 `/clear` 清空，重新开始干净的会话

### 跨会话持久化记忆

通过 `CLAUDE.md` 和 Memory 文件实现：

```
C:\Users\<user>\.claude\projects\<project>\memory\
├── MEMORY.md        # 自动加载，200行内
├── 技术方案.md      # 按主题分类的深度记录
└── 调试经验.md      # 跨会话保留的问题解决方案
```

**写入记忆**：通过 Write 和 Edit 工具更新记忆文件
**读取记忆**：会话开始时 MEMORY.md 自动加载

### 典型使用模式

```
# 会话结束前
"把今天讨论的技术方案保存到记忆文件"

# 新会话开始时
Claude Code 自动加载 MEMORY.md，恢复上下文
```

---

## 附录：Claude Code 快速参考卡

```
┌─────────────────────────────────────────────────────┐
│                   Claude Code 快速参考               │
├─────────────┬───────────────────────────────────────┤
│ 常用命令     │ /clear /model /help /tasks /commit     │
│ 快捷键       │ Alt+T（深度思考）Ctrl+C（中断）         │
│ 模型选择     │ Haiku→快  Sonnet→均衡  Opus→深         │
│ 配置文件     │ CLAUDE.md / settings.json              │
│ 自定义命令   │ .claude/commands/*.md                  │
│ 记忆持久化   │ ~/.claude/projects/<p>/memory/         │
├─────────────┼───────────────────────────────────────┤
│ 适合做什么   │ • 代码生成与修复                        │
│             │ • 多文件重构                             │
│             │ • 自动化 Git 工作流                     │
│             │ • 技术文档生成                           │
│             │ • 复杂分析与规划                         │
│             │ • 并行执行多个子任务                     │
└─────────────┴───────────────────────────────────────┘
```

---

*文档生成日期：2026年2月25日*
*适用版本：Claude Code 最新版（claude.ai/code）*
