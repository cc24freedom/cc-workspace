"""
本地语音转写 MCP Server
使用 faster-whisper 在本地完成音频转写，无需上传至云端
"""

import os
import time
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# ── 配置 ──────────────────────────────────────────────
OUTPUT_DIR = Path(r"e:\CC\项目\tools\meeting_transcripts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 模型缓存（避免重复加载）
_model_cache = {}

mcp = FastMCP("whisper-local")


def _get_model(model_size: str = "medium"):
    """加载并缓存 Whisper 模型"""
    if model_size not in _model_cache:
        from faster_whisper import WhisperModel
        print(f"[Whisper] 首次加载模型 {model_size}，请稍候（约需 30 秒）...")
        _model_cache[model_size] = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"  # CPU 推理最优配置
        )
    return _model_cache[model_size]


@mcp.tool()
def transcribe_audio(
    file_path: str,
    language: str = "zh",
    model_size: str = "medium",
    with_timestamps: bool = False
) -> str:
    """
    本地转写音频文件（完全离线，不上传任何数据）。

    Args:
        file_path: 音频文件绝对路径，支持 mp3、m4a、wav、mp4、webm、flac 等格式
        language:  语言代码，"zh" = 中文（默认），"en" = 英文，"auto" = 自动检测
        model_size: 模型精度，"base"（快）/ "medium"（推荐）/ "large-v3"（最准）
        with_timestamps: 是否在转写文本中附带时间戳，默认 False

    Returns:
        转写文本内容及保存路径
    """
    audio_path = Path(file_path)
    if not audio_path.exists():
        return f"错误：文件不存在 — {file_path}"

    suffix = audio_path.suffix.lower()
    supported = {".mp3", ".m4a", ".wav", ".mp4", ".webm", ".flac", ".ogg", ".aac", ".wma"}
    if suffix not in supported:
        return f"错误：不支持的格式 {suffix}，支持格式：{', '.join(supported)}"

    try:
        model = _get_model(model_size)

        lang = None if language == "auto" else language
        t0 = time.time()

        segments, info = model.transcribe(
            str(audio_path),
            language=lang,
            beam_size=1,              # 1 比 5 快 3-5x，中文准确率损失极小
            vad_filter=True,          # 过滤静音段，提升准确性
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # 收集结果
        lines = []
        full_text_parts = []
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            full_text_parts.append(text)
            if with_timestamps:
                start = f"{int(seg.start // 60):02d}:{seg.start % 60:05.2f}"
                end   = f"{int(seg.end   // 60):02d}:{seg.end   % 60:05.2f}"
                lines.append(f"[{start} → {end}] {text}")
            else:
                lines.append(text)

        elapsed = time.time() - t0
        full_text = "\n".join(lines)

        # 保存转写文本
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = OUTPUT_DIR / f"transcript_{audio_path.stem}_{timestamp}.txt"
        header = (
            f"音频文件：{audio_path.name}\n"
            f"转写时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"检测语言：{info.language}（置信度 {info.language_probability:.0%}）\n"
            f"模型规格：{model_size} | 耗时：{elapsed:.1f}s\n"
            f"{'─' * 60}\n\n"
        )
        out_file.write_text(header + full_text, encoding="utf-8")

        char_count = len("".join(full_text_parts))
        return (
            f"转写完成！共 {char_count} 字，耗时 {elapsed:.1f}s\n"
            f"检测语言：{info.language}（置信度 {info.language_probability:.0%}）\n"
            f"文件已保存：{out_file}\n\n"
            f"{'─' * 60}\n"
            f"{full_text}"
        )

    except Exception as e:
        return f"转写失败：{e}"


@mcp.tool()
def save_meeting_minutes(content: str, filename: str = "") -> str:
    """
    将会议纪要文本保存为 Markdown 文件。

    Args:
        content:  完整的会议纪要 Markdown 文本（由 Claude 整理后传入）
        filename: 文件名（不含路径），如 "2026-03-02_项目周会.md"；为空则自动命名

    Returns:
        保存路径
    """
    if not filename:
        filename = f"会议纪要_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    if not filename.endswith(".md"):
        filename += ".md"

    out_path = OUTPUT_DIR / filename
    out_path.write_text(content, encoding="utf-8")
    return f"会议纪要已保存：{out_path}"


@mcp.tool()
def warm_up(model_size: str = "medium") -> str:
    """预热模型，提前加载到内存，避免首次转写超时。"""
    _get_model(model_size)
    return f"模型 {model_size} 已就绪，可以开始转写"


@mcp.tool()
def list_transcripts() -> str:
    """列出已保存的转写文件和会议纪要。"""
    files = sorted(OUTPUT_DIR.iterdir(), reverse=True)
    if not files:
        return "暂无文件。"

    txts = [f for f in files if f.suffix == ".txt"]
    mds  = [f for f in files if f.suffix == ".md"]

    lines = []
    if txts:
        lines.append(f"── 转写文本（{len(txts)} 份）──")
        for f in txts[:10]:
            size_kb = f.stat().st_size / 1024
            lines.append(f"  {f.name}  ({size_kb:.0f} KB)")
    if mds:
        lines.append(f"\n── 会议纪要（{len(mds)} 份）──")
        for f in mds[:10]:
            size_kb = f.stat().st_size / 1024
            lines.append(f"  {f.name}  ({size_kb:.0f} KB)")

    lines.append(f"\n文件目录：{OUTPUT_DIR}")
    return "\n".join(lines)


if __name__ == "__main__":
    import threading
    # MCP Server 启动时立即在后台线程预热模型，不阻塞 FastMCP 初始化握手
    threading.Thread(target=lambda: _get_model("medium"), daemon=True).start()
    mcp.run()
