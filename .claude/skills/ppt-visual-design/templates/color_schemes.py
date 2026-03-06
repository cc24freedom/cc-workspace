# -*- coding: utf-8 -*-
"""PPT 配色方案库"""
from pptx.dml.color import RGBColor

# 极简风格配色
MINIMALIST_SCHEMES = {
    "business": {
        "primary": RGBColor(44, 62, 80),      # 深灰 #2C3E50
        "accent": RGBColor(52, 152, 219),     # 商务蓝 #3498DB
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(236, 240, 241),
    },
    "tech": {
        "primary": RGBColor(30, 58, 138),     # 深蓝 #1E3A8A
        "accent": RGBColor(249, 115, 22),     # 橙色 #F97316
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(243, 244, 246),
    },
    "academic": {
        "primary": RGBColor(0, 0, 0),         # 黑色
        "accent": RGBColor(107, 114, 128),    # 灰色 #6B7280
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(249, 250, 251),
    }
}

# 商务风格配色
CORPORATE_SCHEMES = {
    "conservative": {
        "primary": RGBColor(30, 58, 138),     # 深蓝
        "accent": RGBColor(156, 163, 175),    # 灰
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(243, 244, 246),
    },
    "modern": {
        "primary": RGBColor(0, 0, 0),         # 黑
        "accent": RGBColor(217, 119, 6),      # 金 #D97706
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(254, 252, 232),
    },
    "tech": {
        "primary": RGBColor(88, 28, 135),     # 深紫 #581C87
        "accent": RGBColor(6, 182, 212),      # 青 #06B6D4
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(240, 253, 250),
    }
}

# 创意风格配色
CREATIVE_SCHEMES = {
    "neon": {
        "primary": RGBColor(0, 0, 0),         # 黑底
        "accent": RGBColor(34, 197, 94),      # 荧光绿 #22C55E
        "secondary": RGBColor(236, 72, 153),  # 荧光粉 #EC4899
        "white": RGBColor(255, 255, 255),
    },
    "gradient": {
        "primary": RGBColor(99, 102, 241),    # 靛蓝 #6366F1
        "accent": RGBColor(236, 72, 153),     # 粉红 #EC4899
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(250, 245, 255),
    },
    "retro": {
        "primary": RGBColor(120, 53, 15),     # 棕褐 #78350F
        "accent": RGBColor(234, 179, 8),      # 黄 #EAB308
        "white": RGBColor(255, 255, 255),
        "light": RGBColor(254, 252, 232),
    }
}

def get_scheme(style, variant="business"):
    """获取配色方案

    Args:
        style: "minimalist", "corporate", "creative"
        variant: 具体变体名称
    """
    schemes = {
        "minimalist": MINIMALIST_SCHEMES,
        "corporate": CORPORATE_SCHEMES,
        "creative": CREATIVE_SCHEMES,
    }
    return schemes.get(style, {}).get(variant, MINIMALIST_SCHEMES["business"])
