#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成系统总体架构SVG图 v2 — 900×790 纵向五层布局"""

W, H = 900, 790
FONT = "Microsoft YaHei,SimHei,sans-serif"
OUT  = r"e:\CC\项目\海上无人集群\系统总体架构图.svg"

def mk():
    el = []
    def add(*s): el.extend(s)

    add('<?xml version="1.0" encoding="UTF-8"?>')
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    add('<defs>')
    add('<marker id="a" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0,10 3.5,0 7" fill="#374151"/></marker>')
    add('<marker id="b" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0,10 3.5,0 7" fill="#2d5c94"/></marker>')
    add('<marker id="c" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0,10 3.5,0 7" fill="#15803d"/></marker>')
    add('</defs>')
    add(f'<rect width="{W}" height="{H}" fill="#eef2f7"/>')

    # ── 标题 ──────────────────────────────────────────────────────
    add('<rect x="20" y="12" width="860" height="40" rx="4" fill="#1a3558"/>')
    add(f'<text x="450" y="37" text-anchor="middle" font-family="{FONT}" '
        f'font-size="16" font-weight="bold" fill="white">'
        '海上作战决策建模数据样本生成与服务系统总体架构</text>')

    # ── 数据来源 ──────────────────────────────────────────────────
    add(f'<text x="450" y="68" text-anchor="middle" font-family="{FONT}" font-size="11" '
        f'fill="#64748b">─── 数据来源 ───</text>')

    # 仿真平台（左）
    add('<rect x="40" y="75" width="320" height="60" rx="5" fill="white" '
        'stroke="#2d5c94" stroke-width="1.5" stroke-dasharray="6,3"/>')
    add(f'<text x="200" y="100" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" font-weight="bold" fill="#2d5c94">仿真平台</text>')
    add(f'<text x="200" y="123" text-anchor="middle" font-family="{FONT}" '
        f'font-size="11" fill="#64748b">冷启动执行环境 · GameState输出</text>')

    # 演习数据（右）
    add('<rect x="540" y="75" width="320" height="60" rx="5" fill="white" '
        'stroke="#15803d" stroke-width="1.5" stroke-dasharray="6,3"/>')
    add(f'<text x="700" y="100" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" font-weight="bold" fill="#15803d">演习 / 开源数据</text>')
    add(f'<text x="700" y="123" text-anchor="middle" font-family="{FONT}" '
        f'font-size="11" fill="#64748b">热启动种子数据</text>')

    add('<line x1="200" y1="135" x2="200" y2="170" stroke="#2d5c94" stroke-width="2" marker-end="url(#b)"/>')
    add('<line x1="700" y1="135" x2="700" y2="170" stroke="#15803d" stroke-width="2" marker-end="url(#c)"/>')

    # ── 规则生成层 ─────────────────────────────────────────────────
    add('<rect x="20" y="175" width="860" height="195" rx="6" fill="#dbeafe" stroke="#2d5c94" stroke-width="2"/>')
    add('<rect x="20" y="175" width="860" height="28" rx="6" fill="#2d5c94"/>')
    add('<rect x="20" y="187" width="860" height="16" fill="#2d5c94"/>')
    add(f'<text x="115" y="195" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" font-weight="bold" fill="white">规 则 生 成 层</text>')

    # 冷启动子框
    add('<rect x="30" y="210" width="400" height="148" rx="5" fill="white" stroke="#3b82f6" stroke-width="1.5"/>')
    add('<rect x="30" y="210" width="400" height="24" rx="5" fill="#3b82f6"/>')
    add('<rect x="30" y="220" width="400" height="14" fill="#3b82f6"/>')
    add(f'<text x="230" y="226" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="white">冷启动（规则引擎驱动仿真生成）</text>')

    add('<rect x="42" y="241" width="180" height="107" rx="4" fill="#eff6ff" stroke="#93c5fd" stroke-width="1"/>')
    add(f'<text x="132" y="261" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="#1e40af">参数化战术规则引擎</text>')
    for dy, s in [(19,"· 5种战术行为类型"), (37,"· 7个参数化控制点位"), (55,"· 网格/随机/边界增强")]:
        add(f'<text x="132" y="{261+dy}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11" fill="#374151">{s}</text>')
    add(f'<text x="132" y="336" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#6b7280">参数矩阵采样策略</text>')

    add('<line x1="222" y1="295" x2="240" y2="295" stroke="#3b82f6" stroke-width="2" marker-end="url(#b)"/>')

    add('<rect x="240" y="241" width="180" height="107" rx="4" fill="#eff6ff" stroke="#93c5fd" stroke-width="1"/>')
    add(f'<text x="330" y="261" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="#1e40af">格式转换→仿真→采集</text>')
    for dy, s in [(19,"· 规则输出→想定格式"), (37,"· 仿真平台加载执行"), (55,"· GameState数据采集")]:
        add(f'<text x="330" y="{261+dy}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11" fill="#374151">{s}</text>')
    add(f'<text x="330" y="336" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#6b7280">字段映射→入库流水线</text>')

    # 热启动子框
    add('<rect x="470" y="210" width="400" height="148" rx="5" fill="white" stroke="#16a34a" stroke-width="1.5"/>')
    add('<rect x="470" y="210" width="400" height="24" rx="5" fill="#16a34a"/>')
    add('<rect x="470" y="220" width="400" height="14" fill="#16a34a"/>')
    add(f'<text x="670" y="226" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="white">热启动（演习数据清洗增强）</text>')

    add('<rect x="482" y="241" width="180" height="107" rx="4" fill="#f0fdf4" stroke="#86efac" stroke-width="1"/>')
    add(f'<text x="572" y="261" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="#15803d">数据清洗程序</text>')
    for dy, s in [(19,"· 字段格式归一化"), (37,"· 异常值处理"), (55,"· 统一数据模式输出")]:
        add(f'<text x="572" y="{261+dy}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11" fill="#374151">{s}</text>')
    add(f'<text x="572" y="336" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#6b7280">三层级数据模式格式</text>')

    add('<line x1="662" y1="295" x2="680" y2="295" stroke="#16a34a" stroke-width="2" marker-end="url(#c)"/>')

    add('<rect x="680" y="241" width="180" height="107" rx="4" fill="#f0fdf4" stroke="#86efac" stroke-width="1"/>')
    add(f'<text x="770" y="261" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="#15803d">参数扰动增强程序</text>')
    for dy, s in [(19,"· 7点位受控扰动"), (37,"· 扩展样本生成"), (55,"· 写入样本数据库")]:
        add(f'<text x="770" y="{261+dy}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11" fill="#374151">{s}</text>')

    # 连接器
    add('<line x1="230" y1="358" x2="230" y2="393" stroke="#2d5c94" stroke-width="2" marker-end="url(#b)"/>')
    add('<line x1="670" y1="358" x2="670" y2="393" stroke="#15803d" stroke-width="2" marker-end="url(#c)"/>')
    add(f'<text x="450" y="382" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#64748b">标准化接口封装  ·  统一写入数据库</text>')

    # ── 数据管理层 ─────────────────────────────────────────────────
    add('<rect x="20" y="398" width="860" height="218" rx="6" fill="#d1fae5" stroke="#059669" stroke-width="2"/>')
    add('<rect x="20" y="398" width="860" height="28" rx="6" fill="#065f46"/>')
    add('<rect x="20" y="410" width="860" height="16" fill="#065f46"/>')
    add(f'<text x="115" y="417" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" font-weight="bold" fill="white">数 据 管 理 层</text>')

    # 三层级数据库
    add('<rect x="30" y="434" width="265" height="168" rx="5" fill="white" stroke="#047857" stroke-width="1.5"/>')
    add('<rect x="30" y="434" width="265" height="24" rx="5" fill="#047857"/>')
    add('<rect x="30" y="446" width="265" height="12" fill="#047857"/>')
    add(f'<text x="162" y="450" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="white">三层级样本数据库</text>')
    for y2, label in [(484,"编队级数据表"), (522,"单舰（平台）级数据表"), (560,"武器装备级数据表")]:
        add(f'<rect x="42" y="{y2-19}" width="241" height="30" rx="3" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1"/>')
        add(f'<text x="162" y="{y2}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="12" fill="#065f46">{label}</text>')
        if y2 < 560:
            add(f'<line x1="162" y1="{y2+11}" x2="162" y2="{y2+19}" '
                f'stroke="#34d399" stroke-width="2" marker-end="url(#a)"/>')
    add(f'<text x="162" y="589" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#6b7280">外键关联 · 数据入库流水线</text>')

    # 数据治理
    add('<rect x="313" y="434" width="220" height="168" rx="5" fill="white" stroke="#c2410c" stroke-width="1.5"/>')
    add('<rect x="313" y="434" width="220" height="24" rx="5" fill="#c2410c"/>')
    add('<rect x="313" y="446" width="220" height="12" fill="#c2410c"/>')
    add(f'<text x="423" y="450" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="white">数据治理</text>')
    for y2, label in [(484,"规模性评价  S_scale"), (522,"多样性评价  S_div"), (560,"价值性评价  S_val")]:
        add(f'<rect x="325" y="{y2-19}" width="196" height="30" rx="3" fill="#fff7ed" stroke="#fb923c" stroke-width="1"/>')
        add(f'<text x="423" y="{y2}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="12" fill="#c2410c">{label}</text>')
    add(f'<text x="423" y="589" text-anchor="middle" font-family="{FONT}" '
        f'font-size="11" fill="#374151">三维综合评分 S_total</text>')

    # 数据服务接口
    add('<rect x="551" y="434" width="319" height="168" rx="5" fill="white" stroke="#6d28d9" stroke-width="1.5"/>')
    add('<rect x="551" y="434" width="319" height="24" rx="5" fill="#6d28d9"/>')
    add('<rect x="551" y="446" width="319" height="12" fill="#6d28d9"/>')
    add(f'<text x="710" y="450" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" fill="white">数据服务接口</text>')
    for bx, by, lines2 in [
        (563, 465, [("典型任务查询","#5b21b6",True), ("按任务/战术/层级","#374151",False),
                    ("多条件组合检索","#374151",False), ("按需抽取样本集合","#6b7280",False)]),
        (716, 465, [("个性化定制","#5b21b6",True), ("自定义参数配置","#374151",False),
                    ("新建决策任务","#374151",False), ("定制数据生成方法","#6b7280",False)]),
    ]:
        add(f'<rect x="{bx}" y="{by}" width="143" height="90" rx="3" fill="#f5f3ff" stroke="#c4b5fd" stroke-width="1"/>')
        for i, (txt, col, bold) in enumerate(lines2):
            fw = "bold" if bold else "normal"
            sz = 12 if i == 0 else (11 if i < 3 else 10)
            add(f'<text x="{bx+71}" y="{by+18+i*19}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="{sz}" font-weight="{fw}" fill="{col}">{txt}</text>')
    add(f'<text x="710" y="589" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="#6b7280">配置文件参数化扩展 · 可替换为模型训练输出接口</text>')

    # ── 向下箭头 ──
    add('<line x1="450" y1="616" x2="450" y2="651" stroke="#374151" stroke-width="2" marker-end="url(#a)"/>')

    # ── Web 前端 ───────────────────────────────────────────────────
    add('<rect x="20" y="655" width="860" height="55" rx="5" fill="#fef9c3" stroke="#ca8a04" stroke-width="2"/>')
    add(f'<text x="450" y="679" text-anchor="middle" font-family="{FONT}" '
        f'font-size="14" font-weight="bold" fill="#78350f">数据管理 Web 前端</text>')
    add(f'<text x="450" y="700" text-anchor="middle" font-family="{FONT}" '
        f'font-size="11" fill="#713f12">数据查询浏览  |  数据生成任务管理  |  数据治理看板</text>')

    add('<line x1="450" y1="710" x2="450" y2="740" stroke="#374151" stroke-width="2" marker-end="url(#a)"/>')

    # ── 使用方 ─────────────────────────────────────────────────────
    add('<rect x="220" y="743" width="460" height="36" rx="5" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>')
    add(f'<text x="450" y="766" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" fill="#334155">研究人员  /  数据管理员</text>')

    add('</svg>')
    return '\n'.join(el)


with open(OUT, 'w', encoding='utf-8') as f:
    f.write(mk())
print(f"OK: {OUT}")
