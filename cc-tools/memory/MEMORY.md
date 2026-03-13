# 工作记忆

## MCP 工具

### 本地语音转写 MCP Server（whisper-local）
- **脚本位置**: `e:\CC\项目\tools\whisper_mcp_server.py`
- **引擎**: faster-whisper 1.2.1（CPU int8），PyAV 自带 ffmpeg，无需系统安装 ffmpeg
- **模型**: 首次调用自动从 HuggingFace 下载（medium ~300MB）
- **输出目录**: `e:\CC\项目\tools\meeting_transcripts\`
- **可用工具**:
  - `transcribe_audio(file_path, language, model_size, with_timestamps)` — 本地转写音频
  - `save_meeting_minutes(content, filename)` — 保存会议纪要 Markdown
  - `list_transcripts()` — 列出已有文件
- **工作流**: `transcribe_audio` 获得文本 → Claude 整理成纪要 → `save_meeting_minutes` 保存

### Gemini 图片生成 MCP Server
- **配置文件**: `d:\cc\.mcp.json`
- **脚本位置**: `d:\cc\项目\tools\gemini_image_server.py`
- **API 代理**: turingai.plus（Gemini 3 Pro Image Preview）
- **输出目录**: `d:\cc\cc-tools\generated_images\`
- **Python 版本**: Python 3.14.3（需要 3.10+）
- **依赖包**: mcp, httpx, pillow（已安装）
- **可用工具**:
  - `generate_image(prompt, aspect_ratio)` — 文生图
  - `edit_image(image_path, prompt)` — 图生图（原图+指令；Gemini 输出固定约1264px宽，自动 LANCZOS 放大回原图尺寸）
  - `list_generated_images()` — 列出已生成图片
- **注意**: 用户希望每次会话直接使用此 MCP 工具生成图片，无需重新确认
- **测试状态**: ✅ 已验证正常工作（2026-03-09）

## 架构图/流程图生成方式

- **首选方案**：用 Python 脚本生成 SVG 矢量图，用户用 Visio 直接打开编辑
- **流程**：Python 拼接 SVG XML → 输出 `.svg` 文件 → Visio「文件→打开」导入
- **优势**：矢量无损、文字/框/箭头在 Visio 中完全可编辑、无清晰度问题
- **注意事项**：
  - 字体用 `Microsoft YaHei, SimHei, sans-serif` 确保中文显示
  - 箭头用 SVG `<marker>` 定义
  - draw.io `.drawio` 格式转 `.vsdx` 后 Visio 无法正常打开，不要用此方案
  - Gemini 生成的图片分辨率有限且不可编辑，仅用于参考/预览，正式图用 SVG 方案

## 文件夹整理规范

用户希望定期整理工作文件夹，固定方式如下：

- **工作文件**（最新版）留在根目录：主文档 .md/.docx/.pdf + 当前架构图 .svg
- **脚本**移入 `scripts/` 子目录（gen_*.py 等）
- **历史版本/归档文件**移入 `archive/` 子目录
- **临时/中间文件删除**：tmp_*.txt、*_extracted.txt、brief_text.txt、pdf_text.txt、template_copy.docx、~$*.docx（Word锁定文件）、原始压缩包（*.zip）
- **操作前**：先列出文件清单，确认分类方案，经用户确认后再执行
- **用 Python** 执行移动/删除操作（Windows 中文路径兼容性最好）

## 写作流程
完整流程见 `e:\CC\项目\memory\writing_workflow.md`
核心步骤：需求输入 → 文档解读 → 大纲确认 → MD起草 → 内容迭代 → 架构图 → Word生成 → 格式调整

## cc-tools Git 同步规范
- **仓库**: `https://github.com/cc24freedom/cc-tools`（私有）
- **本地路径**: `e:\CC\cc-tools\`
- **规则**: 每次修改 cc-tools 目录下的文件后，立即 commit + push，不等用户提醒
- **常用命令**:
  ```powershell
  cd "e:\CC\cc-tools"
  git add <文件>
  git commit -m "简短说明"
  git push
  ```
- **日常记忆同步**（如 MEMORY.md 有更新）:
  ```powershell
  Copy-Item "C:\Users\37948\.claude\projects\e--CC\memory\MEMORY.md" "memory\"
  git add memory\MEMORY.md
  git commit -m "sync: memory $(Get-Date -Format 'yyyy-MM-dd')"
  git push
  ```

## 会话状态自动保存

- **状态文件**: `session_state.md`（同目录）
- **保存时机**: 每次完成重要任务后，Claude 主动更新 `session_state.md`
- **内容**: 当前项目、本次完成的工作、待处理事项、关键决策
- **恢复方式**: 新会话开始时 Claude 自动读取此文件，恢复工作上下文
- **用户也可主动触发**: 说"保存当前状态"即可要求立即更新

## 公司与团队

### 超参数科技（深圳）有限公司
- **核心定位**: AI智能体构建与训练服务商，聚焦军事装备智能化
- **技术团队**: 7人核心团队可支撑双项目并行
- **算力资源**: CPU 9000核@0.04元/核时，GPU A100 15张@5元/卡时，日成本10440元

### 团队成员
- **迟成**（用户本人）- 综合管理岗，负责项目整体推进、对外技术汇报、交付文档管理
- **许壮（壮哥）** - 迟成的直属上级，管理层，项目方案审批、技术方向决策
- **James** - 商务，负责商务拓展、客户关系维护

## Obsidian 知识库

### 知识库结构
- **位置**: `e:\CC` 作为 Obsidian vault 根目录
- **项目笔记**: `项目/[项目名]/项目概览.md`（公司项目）
- **技术笔记**: `知识库/技术/`（公司技术资产）
- **客户笔记**: `知识库/客户/`（公司客户）
- **个人项目**: `知识库/个人项目/`（用户个人工具和side projects）

### 已建立的知识网络（14个笔记）

**客户（4个）**：
- 中国兵器工业集团
- 大连舰艇学院
- 360游戏
- Wargaming

**技术（6个）**：
- 强化学习算法库
- 参数化战术规则引擎
- AI Gamebot技术
- 双模式数据生成框架
- 三层级数据库设计
- 多智能体仿真对抗

**项目（4个）**：
- 海上无人集群项目
- 坦克世界AI Gamebot提案
- 强化学习训练平台
- 装备智能体项目
- 多智能体编队项目

### 我的维护职责

**自动维护场景**：
1. **新项目启动时** → 创建项目概览笔记，链接相关技术和客户
2. **项目状态变化时** → 更新项目概览笔记的状态标签
3. **发现新技术资产时** → 创建技术笔记或更新现有笔记
4. **生成技术文档时** → 在文档中添加 `[[知识库笔记]]` 链接
5. **客户信息更新时** → 更新客户笔记

**维护原则**：
- 保持双向链接的完整性
- 使用统一的标签体系（tags: [项目类型, 状态, 领域]）
- 项目概览笔记必须包含：客户、状态、技术路线、相关技术链接
- 技术笔记必须包含：应用项目列表、相关技术链接

**用户维护**：
- 用户可在 Obsidian 中随时编辑、补充知识库笔记
- 用户编辑后，我在新会话中会读取最新内容

## 当前项目

### SLG AI助手项目（2026-03）
- **项目定位**: 从AI Bot转向AI助手，切入SLG游戏市场
- **技术路线**: LLM驱动（GPT-4/Claude）+ AI Agent框架（类似OpenClaw），非强化学习
- **核心能力**:
  - 大模型决策系统（Tool Calling + Memory）
  - 多智能体协同（联盟场景）
  - 秒级/毫秒级响应时间
- **商业模式**:
  - Phase 1（0-12月）：定制开发，双重收入（定制费100-200万 + 内购分成30%）
  - Phase 2（12月后）：独立App，玩家直接订阅，100%收入归我方
- **交付文档**:
  - `d:\cc\SLG\SLG_AI助手解决方案_技术与商业方案.md`（完整方案30+页）
  - `d:\cc\SLG\SLG_AI助手项目汇报_给壮哥.md`（执行摘要）
- **状态**: 方案已完成，待壮哥决策

## 项目经验案例库

### 工作内容克制案例
**海军项目识别并删除的非必要内容**：
- 节点故障检测、任务重分配、通信超时处理（容错机制，超出当前指标范围）
- 仿真驱动控制器中的并发控制、状态监控、失败重试（工程鲁棒性，非验收要求）
- 测试验证脚本和demo脚本（用户明确："不要自己给自己增加工作内容"）

## 项目基本信息
- 文档仓库，无源代码，交付物为 .docx/.pdf/.pptx/.vsdx
- 详细规范见 CLAUDE.md
