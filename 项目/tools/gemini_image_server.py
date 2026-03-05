"""
Gemini Image Generation MCP Server
通过第三方代理站调用 Gemini API 生成图片
"""

import base64
import os
import time
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

# ── 配置 ──────────────────────────────────────────────
API_BASE = "https://turingai.plus"
API_KEY = "sk-H0FdQNttW5hOITfFofi535RHfw8VovvFWKyTkUHp8rMOYJyZ"
MODEL = "gemini-3-pro-image-preview"
OUTPUT_DIR = Path(r"e:\CC\cc-tools\generated_images")
TIMEOUT = 120  # 秒

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── MCP Server ────────────────────────────────────────
mcp = FastMCP("gemini-image")


@mcp.tool()
async def generate_image(prompt: str, aspect_ratio: str = "1:1") -> str:
    """
    使用 Gemini 生成图片。

    Args:
        prompt: 图片描述（英文效果更好）
        aspect_ratio: 宽高比，如 "1:1", "16:9", "9:16", "4:3", "3:4"

    Returns:
        生成图片的本地文件路径，以及 Gemini 返回的文字说明（如有）
    """
    url = f"{API_BASE}/v1beta/models/{MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "aspectRatio": aspect_ratio,
        },
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        return f"API 请求失败 (HTTP {resp.status_code}): {resp.text}"

    data = resp.json()

    # 解析响应
    candidates = data.get("candidates", [])
    if not candidates:
        return f"API 返回无结果: {data}"

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = []
    image_path = None

    for part in parts:
        if "text" in part:
            text_parts.append(part["text"])
        elif "inlineData" in part:
            mime_type = part["inlineData"].get("mimeType", "image/png")
            ext = mime_type.split("/")[-1].replace("jpeg", "jpg")
            img_bytes = base64.b64decode(part["inlineData"]["data"])

            filename = f"gemini_{int(time.time())}.{ext}"
            image_path = OUTPUT_DIR / filename
            image_path.write_bytes(img_bytes)

    # 组装返回信息
    result_lines = []
    if image_path:
        result_lines.append(f"图片已保存: {image_path}")
    if text_parts:
        result_lines.append(f"文字说明: {''.join(text_parts)}")
    if not result_lines:
        return f"API 返回了未知格式: {data}"

    return "\n".join(result_lines)


@mcp.tool()
async def edit_image(image_path: str, prompt: str) -> str:
    """
    使用 Gemini 编辑已有图片（图生图）。

    Args:
        image_path: 原图绝对路径（jpg/png）
        prompt: 编辑指令（英文效果更好）

    Returns:
        生成图片的本地文件路径，以及 Gemini 返回的文字说明（如有）
    """
    import mimetypes

    path = Path(image_path)
    if not path.exists():
        return f"文件不存在: {image_path}"

    img_bytes = path.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode()
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"

    url = f"{API_BASE}/v1beta/models/{MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"inlineData": {"mimeType": mime, "data": img_b64}},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        return f"API 请求失败 (HTTP {resp.status_code}): {resp.text}"

    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        return f"API 返回无结果: {data}"

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = []
    image_path_out = None

    for part in parts:
        if "text" in part:
            text_parts.append(part["text"])
        elif "inlineData" in part:
            from PIL import Image
            import io
            mime_type = part["inlineData"].get("mimeType", "image/png")
            ext = mime_type.split("/")[-1].replace("jpeg", "jpg")
            img_out = base64.b64decode(part["inlineData"]["data"])

            # 放大回原图尺寸，保持清晰度一致
            orig_size = Image.open(path).size  # (width, height)
            edited_img = Image.open(io.BytesIO(img_out))
            if edited_img.size != orig_size:
                edited_img = edited_img.resize(orig_size, Image.LANCZOS)

            filename = f"edited_{int(time.time())}.jpg"
            image_path_out = OUTPUT_DIR / filename
            edited_img.save(str(image_path_out), "JPEG", quality=95)

    result_lines = []
    if image_path_out:
        result_lines.append(f"图片已保存: {image_path_out}")
    if text_parts:
        result_lines.append(f"文字说明: {''.join(text_parts)}")
    if not result_lines:
        return f"API 返回了未知格式: {data}"

    return "\n".join(result_lines)


@mcp.tool()
async def list_generated_images() -> str:
    """列出已生成的所有图片文件。"""
    files = sorted(OUTPUT_DIR.glob("gemini_*"), reverse=True)
    if not files:
        return "暂无已生成的图片。"
    lines = [f"共 {len(files)} 张图片:"]
    for f in files[:20]:  # 最多显示最近20张
        size_kb = f.stat().st_size / 1024
        lines.append(f"  {f.name} ({size_kb:.0f} KB) - {f}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
