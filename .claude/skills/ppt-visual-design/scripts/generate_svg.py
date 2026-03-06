#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG 架构图生成脚本
生成可在 Visio 中编辑的 SVG 矢量图
"""

import sys
import json

def generate_layered_architecture(layers, output_path, colors):
    """
    生成分层架构图

    Args:
        layers: 层级列表 [{"name": "感知层", "modules": ["模块1", "模块2"]}, ...]
        output_path: 输出路径
        colors: 配色方案
    """
    width = 800
    height = 600
    layer_height = height / len(layers)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
    <style>
        .layer-box {{ fill: {colors['primary']}; stroke: {colors['secondary']}; stroke-width: 2; }}
        .layer-text {{ fill: white; font-family: Microsoft YaHei, SimHei, sans-serif; font-size: 20px; font-weight: bold; }}
        .module-box {{ fill: {colors['secondary']}; stroke: {colors['accent']}; stroke-width: 1; }}
        .module-text {{ fill: white; font-family: Microsoft YaHei, SimHei, sans-serif; font-size: 14px; }}
    </style>
</defs>
'''

    for i, layer in enumerate(layers):
        y = i * layer_height

        # 层级背景
        svg += f'<rect class="layer-box" x="50" y="{y + 20}" width="700" height="{layer_height - 40}" rx="10"/>\n'

        # 层级名称
        svg += f'<text class="layer-text" x="400" y="{y + 50}" text-anchor="middle">{layer["name"]}</text>\n'

        # 模块
        modules = layer.get('modules', [])
        if modules:
            module_width = 600 / len(modules)
            for j, module in enumerate(modules):
                mx = 100 + j * module_width
                my = y + 70
                svg += f'<rect class="module-box" x="{mx}" y="{my}" width="{module_width - 20}" height="50" rx="5"/>\n'
                svg += f'<text class="module-text" x="{mx + module_width/2 - 10}" y="{my + 30}" text-anchor="middle">{module}</text>\n'

    svg += '</svg>'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"SVG 已生成：{output_path}")

def generate_flowchart(steps, output_path, colors):
    """
    生成横向流程图

    Args:
        steps: 步骤列表 ["步骤1", "步骤2", ...]
        output_path: 输出路径
        colors: 配色方案
    """
    width = 1000
    height = 300
    step_width = (width - 100) / len(steps)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="{colors['accent']}" />
    </marker>
    <style>
        .step-box {{ fill: {colors['primary']}; stroke: {colors['secondary']}; stroke-width: 2; }}
        .step-text {{ fill: white; font-family: Microsoft YaHei, SimHei, sans-serif; font-size: 16px; text-anchor: middle; }}
        .arrow {{ stroke: {colors['accent']}; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }}
    </style>
</defs>
'''

    for i, step in enumerate(steps):
        x = 50 + i * step_width

        # 步骤框
        svg += f'<rect class="step-box" x="{x}" y="100" width="{step_width - 60}" height="80" rx="10"/>\n'
        svg += f'<text class="step-text" x="{x + (step_width - 60)/2}" y="145">{step}</text>\n'

        # 箭头
        if i < len(steps) - 1:
            x1 = x + step_width - 60
            x2 = x + step_width - 10
            svg += f'<line class="arrow" x1="{x1}" y1="140" x2="{x2}" y2="140"/>\n'

    svg += '</svg>'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"SVG 已生成：{output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python generate_svg.py <config.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        config = json.load(f)

    diagram_type = config['type']
    colors = config['colors']
    output_path = config['output_path']

    if diagram_type == 'layered':
        generate_layered_architecture(config['layers'], output_path, colors)
    elif diagram_type == 'flowchart':
        generate_flowchart(config['steps'], output_path, colors)
    else:
        print(f"不支持的图表类型：{diagram_type}")
