# -*- coding: utf-8 -*-
"""
将PPT每页导出为PNG图片，用于AI视觉评审
"""
import os
import sys
import win32com.client

def ppt_to_images(ppt_path, output_dir):
    """
    将PPT每页导出为PNG图片

    Args:
        ppt_path: PPT文件路径
        output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 转换为绝对路径
    ppt_path = os.path.abspath(ppt_path)
    output_dir = os.path.abspath(output_dir)

    print(f"正在打开PPT: {ppt_path}")

    # 启动PowerPoint
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1

    try:
        # 打开PPT
        pres = powerpoint.Presentations.Open(ppt_path, ReadOnly=1)

        print(f"PPT共有 {pres.Slides.Count} 页")

        # 导出每一页
        for i in range(1, pres.Slides.Count + 1):
            slide = pres.Slides(i)
            output_path = os.path.join(output_dir, f"slide_{i:02d}.png")
            slide.Export(output_path, "PNG", 1920, 1080)  # 1920x1080分辨率
            print(f"已导出: slide_{i:02d}.png")

        # 关闭PPT
        pres.Close()
        print(f"\n所有页面已导出到: {output_dir}")

    finally:
        # 退出PowerPoint
        powerpoint.Quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ppt_to_images.py <PPT文件路径> [输出目录]")
        sys.exit(1)

    ppt_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./ppt_screenshots"

    if not os.path.exists(ppt_path):
        print(f"错误: 文件不存在 {ppt_path}")
        sys.exit(1)

    ppt_to_images(ppt_path, output_dir)
