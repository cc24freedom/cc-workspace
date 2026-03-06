# -*- coding: utf-8 -*-
"""PPT 模板库

使用示例：
    from templates import minimalist, corporate, creative
    from templates.color_schemes import get_scheme

    # 极简风格
    minimalist.minimalist_cover(prs, "标题", "副标题", "公司", variant="business")

    # 商务风格
    corporate.corporate_cover(prs, "标题", "副标题", "公司", variant="conservative")

    # 创意风格
    creative.creative_dark_cover(prs, "标题", "副标题", variant="neon")
"""

from . import color_schemes
from . import minimalist
from . import corporate
from . import creative

__all__ = ['color_schemes', 'minimalist', 'corporate', 'creative']
