# MCP 工具使用说明

## 配置状态

✅ `.mcp.json` 已配置完成
✅ MCP 服务器脚本路径已更新
✅ 输出目录已创建

---

## 可用的 MCP 工具

### 1. Gemini 图片生成 (gemini-image)

**功能**：使用 Gemini API 生成图片

**可用工具**：
- `generate_image(prompt, aspect_ratio)` - 文生图
- `edit_image(image_path, prompt)` - 图生图
- `list_generated_images()` - 列出已生成图片

**使用示例**：
```
请用 Gemini 生成一张图片：一只可爱的橙色猫咪坐在窗台上看风景
```

**输出目录**：`d:\cc\cc-tools\generated_images\`

**配置**：
- API 地址：https://turingai.plus
- 模型：gemini-3-pro-image-preview
- 超时：120秒

---

### 2. Whisper 本地语音转写 (whisper-local)

**功能**：本地语音转文字（无需联网）

**可用工具**：
- `transcribe_audio(file_path, language, model_size, with_timestamps)` - 转写音频
- `save_meeting_minutes(content, filename)` - 保存会议纪要
- `list_transcripts()` - 列出已有转写文件

**使用示例**：
```
请转写这个音频文件：d:\recordings\meeting.mp3
```

**输出目录**：`d:\cc\项目\tools\meeting_transcripts\`

**配置**：
- 引擎：faster-whisper 1.2.1
- 模型：medium（首次使用自动下载）
- 语言：自动检测或指定

---

### 3. Obsidian 知识库 (obsidian)

**功能**：与 Obsidian 知识库交互

**前提条件**：
- Obsidian 需要安装 REST API 插件
- 插件需要配置 API Key 和端口

**配置**：
- API URL：http://localhost:27123
- API Key：已配置

---

## 如何使用 MCP 工具

### 方法 1：直接对话调用

在 Claude Code 对话中直接描述需求，Claude 会自动调用相应的 MCP 工具：

```
用户：请用 Gemini 生成一张科技感的 AI 机器人图片
Claude：[自动调用 gemini-image 的 generate_image 工具]
```

### 方法 2：明确指定工具

```
用户：使用 whisper-local 转写 d:\audio\meeting.mp3
Claude：[调用 whisper-local 的 transcribe_audio 工具]
```

---

## 测试 MCP 工具

### 测试 Gemini 图片生成

```
请用 Gemini 生成一张图片：
- 主题：一只橙色的猫咪
- 场景：坐在窗台上看外面的风景
- 风格：温馨、治愈系
- 比例：16:9
```

### 测试 Whisper 语音转写

```
请转写这个音频文件：[提供音频文件路径]
语言：中文
需要时间戳：是
```

---

## 故障排查

### MCP 工具无法使用

1. **检查 VSCode 是否重启**
   - 修改 `.mcp.json` 后需要重启 VSCode

2. **检查 Python 依赖**
   ```bash
   python -c "import httpx, faster_whisper, anthropic; print('依赖正常')"
   ```

3. **检查输出目录权限**
   ```bash
   ls -la d:\cc\cc-tools\generated_images
   ls -la d:\cc\项目\tools\meeting_transcripts
   ```

4. **查看 Claude Code 日志**
   - VSCode → 输出 → 选择 "Claude Code"

---

## 注意事项

1. **Gemini 图片生成**
   - 需要网络连接（通过代理）
   - API Key 有效期需要定期检查
   - 生成时间较长（可能需要 30-60 秒）

2. **Whisper 语音转写**
   - 首次使用会下载模型（约 300MB）
   - 完全本地运行，无需联网
   - 转写速度取决于 CPU 性能

3. **Python 版本限制**
   - 当前 Python 3.9.1
   - 部分功能可能需要 Python 3.10+

---

## 配置文件位置

- MCP 配置：`d:\cc\.mcp.json`
- Gemini 脚本：`d:\cc\项目\tools\gemini_image_server.py`
- Whisper 脚本：`d:\cc\项目\tools\whisper_mcp_server.py`
- 新闻配置：`d:\cc\项目\tools\news_config.json`
