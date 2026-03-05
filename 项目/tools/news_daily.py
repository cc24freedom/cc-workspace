# -*- coding: utf-8 -*-
"""
每日 AI & 军工新闻自动整理 v2

用法:
    python news_daily.py            # 正常运行（今天已存在则跳过）
    python news_daily.py --force    # 强制重新生成今日文件
    python news_daily.py --learn    # 扫描所有日报中的 ⭐ 标记，更新兴趣偏好

标记喜欢的文章：在 news/YYYY-MM-DD.md 中，在文章标题行行首加 ⭐，例如：
    ⭐ **[标题](url)**  `来源`

输出:
    e:\\CC\\项目\\news\\YYYY-MM-DD.md   每日新闻（含 AI 摘要、来源标签）
    e:\\CC\\项目\\news\\README.md       目录索引
    e:\\CC\\项目\\tools\\preferences.json  用户兴趣偏好

依赖:
    pip install feedparser beautifulsoup4 httpx
"""

import sys
import json
import re
import argparse
from datetime import date
from pathlib import Path

import feedparser
import httpx
from bs4 import BeautifulSoup

# ── 路径常量 ──────────────────────────────────────────────────────────────────
TOOLS_DIR   = Path(__file__).parent
CONFIG_PATH = TOOLS_DIR / 'news_config.json'
PREFS_PATH  = TOOLS_DIR / 'preferences.json'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
    )
}
HTTP_TIMEOUT = 15


# ── 配置 & 偏好加载 ────────────────────────────────────────────────────────────
def load_config() -> dict:
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)

def load_prefs() -> dict:
    if PREFS_PATH.exists():
        with open(PREFS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {"boosted_keywords": [], "boosted_sources": [],
            "avoided_keywords": [], "liked_articles": []}

def save_prefs(prefs: dict):
    with open(PREFS_PATH, 'w', encoding='utf-8') as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


# ── 深度内容过滤 ───────────────────────────────────────────────────────────────
def is_depth_article(title: str, cfg: dict) -> bool:
    """返回 False 表示是快讯/简讯，应被过滤。"""
    flash_kw = cfg.get('flash_keywords', [])
    min_len  = cfg.get('min_title_length', 12)

    if len(title) < min_len:
        return False
    if any(kw in title for kw in flash_kw):
        return False
    # 数字+月/日 开头的时间型快讯，如 "3月3日..."
    if re.match(r'^\d+[月日]', title):
        return False
    return True


# ── 偏好评分 ───────────────────────────────────────────────────────────────────
def preference_score(item: dict, prefs: dict) -> int:
    """根据用户偏好为文章评分，用于同类别内排序。"""
    score = 0
    title  = item.get('title', '')
    source = item.get('source', '')
    for kw in prefs.get('boosted_keywords', []):
        if kw in title:
            score += 1
    if source in prefs.get('boosted_sources', []):
        score += 2
    return score


# ── RSS 抓取 ───────────────────────────────────────────────────────────────────
def fetch_rss(url: str, source_name: str, n: int,
              keywords: list | None, cfg: dict) -> list[dict]:
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f'  [RSS ERR] {source_name}: {e}')
        return []

    avoided = cfg.get('avoided_keywords', [])  # 来自 preferences（调用时传入）
    items = []
    for entry in feed.entries:
        title = entry.get('title', '').strip()
        link  = entry.get('link', '').strip()
        if not title or not link:
            continue
        if keywords and not any(kw in title for kw in keywords):
            continue
        # 过滤 36氪 newsflashes 等快讯 URL
        if '/newsflashes/' in link:
            continue
        if not is_depth_article(title, cfg):
            continue
        if any(av in title for av in avoided):
            continue
        items.append({'title': title, 'url': link, 'source': source_name})
        if len(items) >= n:
            break

    print(f'  [RSS] {source_name}: {len(items)} 条')
    return items


# ── 英文 RSS 抓取 ─────────────────────────────────────────────────────────────
def fetch_english_rss(url: str, source_name: str, n: int, cfg: dict) -> list[dict]:
    """抓取英文 RSS，按关键词白名单过滤，标记 lang=en。"""
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f'  [RSS ERR] {source_name}: {e}')
        return []

    en_kw = [kw.lower() for kw in cfg.get('english_keywords', [])]
    items = []
    for entry in feed.entries:
        title = entry.get('title', '').strip()
        link  = entry.get('link', '').strip()
        if not title or not link:
            continue
        if len(title) < 30:
            continue
        if en_kw and not any(kw in title.lower() for kw in en_kw):
            continue
        items.append({'title': title, 'url': link, 'source': source_name, 'lang': 'en'})
        if len(items) >= n:
            break

    print(f'  [RSS] {source_name}: {len(items)} 条')
    return items


# ── HTML 抓取：观察者网军事 ────────────────────────────────────────────────────
def fetch_guancha_mil(n: int, cfg: dict) -> list[dict]:
    try:
        r = httpx.get('https://www.guancha.cn/military-afairs/',
                      headers=HEADERS, timeout=HTTP_TIMEOUT, follow_redirects=True)
    except Exception as e:
        print(f'  [HTML ERR] 观察者网: {e}')
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    seen, items = set(), []
    for a in soup.find_all('a', href=True):
        href  = a['href']
        title = a.get_text(strip=True)
        if '/military-affairs/' not in href or len(title) < 8:
            continue
        if re.match(r'^阅读\s*\d+', title):
            continue
        if not is_depth_article(title, cfg):
            continue
        href = href.split('?')[0]
        if not href.startswith('http'):
            href = 'https://www.guancha.cn' + href
        if title in seen:
            continue
        seen.add(title)
        items.append({'title': title, 'url': href, 'source': '观察者网'})
        if len(items) >= n:
            break

    print(f'  [HTML] 观察者网: {len(items)} 条')
    return items


# ── HTML 抓取：中国军网 ────────────────────────────────────────────────────────
def fetch_81cn(n: int, keywords: list, cfg: dict) -> list[dict]:
    try:
        r = httpx.get('http://www.81.cn/', headers=HEADERS,
                      timeout=HTTP_TIMEOUT, follow_redirects=True)
    except Exception as e:
        print(f'  [HTML ERR] 中国军网: {e}')
        return []

    exclude_kw = ['出版', '发行', '精神', '风采', '履职', '论坛', '雷锋',
                  '弘扬', '传承', '思想', '政绩', '记事', '巡礼', '书记']
    soup = BeautifulSoup(r.text, 'html.parser')
    seen, items = set(), []
    for a in soup.find_all('a', href=True):
        href  = a.get('href', '')
        title = a.get_text(strip=True)
        if (not href.startswith('http://www.81.cn/')
                or not any(kw in title for kw in keywords)
                or any(ex in title for ex in exclude_kw)
                or not is_depth_article(title, cfg)
                or title in seen):
            continue
        seen.add(title)
        items.append({'title': title, 'url': href, 'source': '中国军网'})
        if len(items) >= n:
            break

    print(f'  [HTML] 中国军网: {len(items)} 条')
    return items


# ── 新闻汇总 ───────────────────────────────────────────────────────────────────
def collect_all_news(cfg: dict, prefs: dict) -> dict[str, list[dict]]:
    n      = cfg.get('max_items_per_source', 8)
    ai_kw  = cfg.get('ai_keywords', [])
    mil_kw = cfg.get('military_keywords', [])
    # 把用户屏蔽词传给各抓取函数
    cfg_with_avoided = {**cfg, 'avoided_keywords': prefs.get('avoided_keywords', [])}

    print('[抓取] AI 新闻...')
    ai_news = (
        fetch_rss('https://www.qbitai.com/feed', '量子位', n, None,      cfg_with_avoided)
        + fetch_rss('https://36kr.com/feed',     '36氪',   n, ai_kw,     cfg_with_avoided)
        + fetch_rss('https://rss.huxiu.com/',    '虎嗅',   n, ai_kw,     cfg_with_avoided)
    )

    print('[抓取] 军工新闻...')
    mil_news = (
        fetch_guancha_mil(n, cfg_with_avoided)
        + fetch_81cn(n, mil_kw, cfg_with_avoided)
    )

    print('[抓取] 英文精选...')
    en_news = (
        fetch_english_rss('https://www.technologyreview.com/feed/', 'MIT Tech Review', 2, cfg)
        + fetch_english_rss('https://warontherocks.com/feed/',      'War on the Rocks', 2, cfg)
        + fetch_english_rss('https://www.defenseone.com/rss/all/',  'Defense One',      2, cfg)
    )
    en_news = en_news[:3]

    # 按偏好评分排序（高分在前），各类目截断为5条，但保证每个来源至少1条
    def cap_with_diversity(items: list[dict], limit: int) -> list[dict]:
        """截断到 limit 条，但每个 source 至少保留 1 条。"""
        sorted_items = sorted(items, key=lambda x: preference_score(x, prefs), reverse=True)
        # 先每个来源取1条
        seen_sources, reserved = set(), []
        for it in sorted_items:
            if it['source'] not in seen_sources:
                reserved.append(it)
                seen_sources.add(it['source'])
        # 剩余位置用高分条目填满
        rest = [it for it in sorted_items if it not in reserved]
        return (reserved + rest)[:limit]

    ai_news  = cap_with_diversity(ai_news, 5)
    mil_news = cap_with_diversity(mil_news, 5)

    return {'AI新闻': ai_news, '军工新闻': mil_news, '英文精选': en_news}


# ── AI 摘要（Anthropic Messages API）─────────────────────────────────────────
def _summarize_batch(items: list[dict], offset: int, cfg: dict) -> list[dict]:
    """对一批文章调用 API 生成摘要，offset 是全局编号起点。"""
    api_key  = cfg['api_key']
    base_url = cfg['api_base_url']
    model    = cfg.get('model', 'claude-haiku-4-5-20251001')

    numbered = '\n'.join(f'{offset+i+1}. {it["title"]}' for i, it in enumerate(items))

    # 标注哪些条目是英文标题
    en_ids = [offset+i+1 for i, it in enumerate(items) if it.get('lang') == 'en']
    en_note = ''
    if en_ids:
        en_note = f'\n注意：编号 {", ".join(map(str, en_ids))} 为英文标题，请理解后用中文写摘要，说明核心观点。'

    prompt = (
        f'请为以下 {len(items)} 条文章各生成一句话摘要（20-40字），'
        f'说明核心内容，不要重复标题文字。{en_note}\n'
        f'严格以 JSON 格式输出，数组每个元素含 "id"（从{offset+1}开始）和 "summary" 字段。\n\n'
        f'{numbered}'
    )
    resp = httpx.post(
        base_url,
        headers={'Authorization': f'Bearer {api_key}', 'anthropic-version': '2023-06-01'},
        json={'model': model, 'messages': [{'role': 'user', 'content': prompt}],
              'max_tokens': 1200},
        timeout=40
    )
    resp.raise_for_status()
    raw = resp.json()['content'][0]['text'].strip()
    m = re.search(r'\[.*\]', raw, re.S)
    if not m:
        raise ValueError(f'响应未含 JSON 数组，内容：{raw[:100]}')
    parsed = json.loads(m.group())
    # 优先按 id 匹配，退回按顺序
    if parsed and 'id' in parsed[0]:
        summary_map = {e['id']: e.get('summary', '') for e in parsed}
        return [{**it, 'summary': summary_map.get(offset + i + 1, '')} for i, it in enumerate(items)]
    else:
        return [{**it, 'summary': parsed[i].get('summary', '') if i < len(parsed) else ''}
                for i, it in enumerate(items)]


def summarize(items: list[dict], cfg: dict) -> list[dict]:
    api_key  = cfg.get('api_key', '')
    base_url = cfg.get('api_base_url', '')
    if not api_key or not base_url:
        print('[摘要] 未配置 API，跳过')
        return [{**it, 'summary': ''} for it in items]

    BATCH = 15  # 每批最多 15 条，避免 token 超限
    result = []
    try:
        for start in range(0, len(items), BATCH):
            batch = items[start:start + BATCH]
            result.extend(_summarize_batch(batch, start, cfg))
        print(f'[摘要] 完成 {len(result)} 条')
    except Exception as e:
        print(f'[摘要 ERR] {e}，跳过摘要')
        return [{**it, 'summary': ''} for it in items]
    return result


# ── 今日必读：AI 从所有文章中选出最值得读的1条 ─────────────────────────────────
def pick_top_story(all_items: list[dict], cfg: dict) -> dict | None:
    """从所有已摘要的文章中选出当天最值得读的1条。"""
    api_key  = cfg.get('api_key', '')
    base_url = cfg.get('api_base_url', '')
    model    = cfg.get('model', 'claude-haiku-4-5-20251001')
    if not api_key or not base_url or not all_items:
        return None

    numbered = '\n'.join(
        f'{i+1}. [{it["source"]}] {it["title"]}' for i, it in enumerate(all_items)
    )
    prompt = (
        f'以下是今日 {len(all_items)} 条新闻，请选出最值得深度阅读的1条（综合考虑：洞察深度、'
        f'对AI/军事技术方向的参考价值、信息密度）。\n'
        f'以 JSON 格式输出，字段：{{"id": 编号, "reason": "推荐理由，20字以内"}}\n\n'
        f'{numbered}'
    )
    try:
        resp = httpx.post(
            base_url,
            headers={'Authorization': f'Bearer {api_key}', 'anthropic-version': '2023-06-01'},
            json={'model': model, 'messages': [{'role': 'user', 'content': prompt}],
                  'max_tokens': 120},
            timeout=20
        )
        resp.raise_for_status()
        raw = resp.json()['content'][0]['text'].strip()
        m = re.search(r'\{.*\}', raw, re.S)
        if not m:
            return None
        result = json.loads(m.group())
        idx = int(result.get('id', 0)) - 1
        if 0 <= idx < len(all_items):
            return {**all_items[idx], 'reason': result.get('reason', '')}
    except Exception as e:
        print(f'[今日必读 ERR] {e}')
    return None


# ── 格式化日报 ────────────────────────────────────────────────────────────────
def format_daily(today: date, news: dict[str, list[dict]], prefs: dict,
                 top_story: dict | None = None) -> str:
    boosted = prefs.get('boosted_keywords', [])
    lines   = [f'# AI & 军工日报 · {today.strftime("%Y-%m-%d")}\n']

    if boosted:
        lines.append(f'> 当前关注方向：{" / ".join(boosted[:8])}\n')

    # 今日必读
    if top_story:
        lines.append('## 今日必读\n')
        reason = f'　{top_story["reason"]}' if top_story.get('reason') else ''
        lines.append(f'🔥 **[{top_story["title"]}]({top_story["url"]})**  `{top_story["source"]}`')
        if top_story.get('summary'):
            lines.append(f'> {top_story["summary"]}{reason}\n')
        else:
            lines.append(f'>{reason}\n')
        lines.append('---\n')

    for category, items in news.items():
        lines.append(f'## {category}\n')
        if not items:
            lines.append('_今日暂无相关深度内容_\n')
            continue
        for it in items:
            score = preference_score(it, prefs)
            star  = '⭐ ' if score >= 2 else ''
            lines.append(f'{star}**[{it["title"]}]({it["url"]})**  `{it["source"]}`')
            if it.get('summary'):
                lines.append(f'> {it["summary"]}\n')
            else:
                lines.append('')
        lines.append('---\n')

    lines.append(f'_生成时间：{today.strftime("%Y-%m-%d")} · 来源：量子位 / 36氪 / 虎嗅 / 观察者网 / 中国军网 / MIT Tech Review / War on the Rocks / Defense One_')
    lines.append('_喜欢某篇文章？在标题行行首加 ⭐，然后运行 `python news_daily.py --learn` 更新偏好_')
    return '\n'.join(lines)


# ── 保存日报 & 更新索引 ────────────────────────────────────────────────────────
def save_daily(news_dir: Path, today: date, content: str) -> Path:
    news_dir.mkdir(parents=True, exist_ok=True)
    out = news_dir / f'{today.strftime("%Y-%m-%d")}.md'
    out.write_text(content, encoding='utf-8')
    print(f'[保存] {out}')
    return out

def update_index(news_dir: Path, today: date, counts: dict[str, int]):
    index_path = news_dir / 'README.md'
    date_str   = today.strftime('%Y-%m-%d')
    counts_str = ' / '.join(f'{cat} {n}条' for cat, n in counts.items())
    new_row    = f'| [{date_str}]({date_str}.md) | {counts_str} |'

    if not index_path.exists():
        header = '# 新闻日报目录\n\n| 日期 | 新闻数量 |\n|------|----------|\n'
        index_path.write_text(header + new_row + '\n', encoding='utf-8')
        print(f'[索引] 创建 {index_path}')
        return

    text = index_path.read_text(encoding='utf-8')
    if date_str in text:
        # 更新已有行
        lines = text.splitlines(keepends=True)
        for idx, l in enumerate(lines):
            if date_str in l and l.startswith('|'):
                lines[idx] = new_row + '\n'
                break
        index_path.write_text(''.join(lines), encoding='utf-8')
        print(f'[索引] 已更新今日条目')
        return

    lines = text.splitlines(keepends=True)
    insert_at = next((i + 1 for i, l in enumerate(lines) if l.startswith('|---')), len(lines))
    lines.insert(insert_at, new_row + '\n')
    index_path.write_text(''.join(lines), encoding='utf-8')
    print(f'[索引] 已追加 {index_path}')


# ── --learn：扫描 ⭐ 更新偏好 ──────────────────────────────────────────────────
def learn_from_likes(cfg: dict, prefs: dict, silent: bool = False):
    """扫描所有日报中的 ⭐ 文章，提取关键词，更新 preferences.json。
    silent=True 时，若没有新点赞则不打印任何内容。"""
    news_dir  = Path(cfg.get('news_dir'))
    known_urls = {a['url'] for a in prefs.get('liked_articles', [])}

    # 扫描所有 YYYY-MM-DD.md 文件
    new_articles = []
    for md_file in sorted(news_dir.glob('????-??-??.md')):
        file_date = md_file.stem
        text = md_file.read_text(encoding='utf-8')
        for line in text.splitlines():
            # 匹配 ⭐ 开头的文章行
            m = re.match(r'^⭐\s+\*\*\[(.+?)\]\((.+?)\)\*\*\s*`(.+?)`', line)
            if not m:
                continue
            title, url, source = m.group(1), m.group(2), m.group(3)
            if url in known_urls:
                continue
            new_articles.append({'title': title, 'url': url,
                                  'source': source, 'date': file_date})
            known_urls.add(url)

    if not new_articles:
        if not silent:
            print('[学习] 没有发现新的 ⭐ 文章（已全部处理过）')
        return

    print(f'[学习] 发现 {len(new_articles)} 篇新点赞文章，正在提取关键词...')

    # 调用 API 提取关键词
    titles_text = '\n'.join(f'{i+1}. {a["title"]}' for i, a in enumerate(new_articles))
    prompt = (
        f'以下是用户感兴趣的 {len(new_articles)} 篇文章标题，'
        f'请从中提取 5-10 个最能代表用户兴趣方向的中文关键词（2-6字的词组）。\n'
        f'以 JSON 格式输出，字段名为 "keywords"，值为字符串数组。\n\n'
        f'{titles_text}'
    )

    new_keywords = []
    api_key  = cfg.get('api_key', '')
    base_url = cfg.get('api_base_url', '')
    model    = cfg.get('model', 'claude-haiku-4-5-20251001')
    if api_key and base_url:
        try:
            resp = httpx.post(
                base_url,
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'anthropic-version': '2023-06-01',
                },
                json={'model': model,
                      'messages': [{'role': 'user', 'content': prompt}],
                      'max_tokens': 256},
                timeout=20
            )
            resp.raise_for_status()
            raw = resp.json()['content'][0]['text'].strip()
            m   = re.search(r'\{.*\}', raw, re.S)
            if m:
                new_keywords = json.loads(m.group()).get('keywords', [])
        except Exception as e:
            print(f'[学习 ERR] API 调用失败: {e}，仅保存点赞记录')

    # 更新偏好
    existing_kw = set(prefs.get('boosted_keywords', []))
    added_kw    = [kw for kw in new_keywords if kw not in existing_kw]
    prefs['boosted_keywords'] = list(existing_kw) + added_kw

    # 统计点赞来源，高频来源加入 boosted_sources
    from collections import Counter
    all_liked   = prefs.get('liked_articles', []) + new_articles
    source_cnt  = Counter(a['source'] for a in all_liked)
    top_sources = [s for s, c in source_cnt.most_common() if c >= 2]
    prefs['boosted_sources'] = top_sources

    prefs['liked_articles'] = all_liked
    save_prefs(prefs)

    print(f'[学习] 新增关键词：{added_kw}')
    print(f'[学习] 当前关注方向：{prefs["boosted_keywords"]}')
    print(f'[学习] 偏好来源：{prefs["boosted_sources"]}')
    print(f'[学习] 累计点赞文章：{len(all_liked)} 篇')


# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='每日 AI & 军工新闻整理 v2')
    parser.add_argument('--force', action='store_true', help='强制重新生成今日文件')
    parser.add_argument('--learn', action='store_true', help='扫描 ⭐ 更新兴趣偏好（不生成日报）')
    args = parser.parse_args()

    cfg   = load_config()
    prefs = load_prefs()

    if args.learn:
        learn_from_likes(cfg, prefs)
        return

    news_dir = Path(cfg.get('news_dir'))
    today    = date.today()
    out_path = news_dir / f'{today.strftime("%Y-%m-%d")}.md'

    if out_path.exists() and not args.force:
        print(f'[跳过] 今日文件已存在: {out_path}')
        print('  使用 --force 强制重新生成')
        return

    # 0. 自动学习前一天的 ⭐ 标记（有新点赞才打印）
    learn_from_likes(cfg, prefs, silent=True)
    prefs = load_prefs()  # 重新加载，确保用最新偏好抓取

    # 1. 抓取
    all_news = collect_all_news(cfg, prefs)

    # 2. 摘要（全部条目一起批量）
    all_items = all_news['AI新闻'] + all_news['军工新闻'] + all_news['英文精选']
    if all_items:
        summarized        = summarize(all_items, cfg)
        ai_count          = len(all_news['AI新闻'])
        mil_count         = len(all_news['军工新闻'])
        all_news['AI新闻']   = summarized[:ai_count]
        all_news['军工新闻']  = summarized[ai_count:ai_count + mil_count]
        all_news['英文精选']  = summarized[ai_count + mil_count:]

    # 3. 选出今日必读
    all_summarized = all_news['AI新闻'] + all_news['军工新闻'] + all_news['英文精选']
    top_story = pick_top_story(all_summarized, cfg)
    if top_story:
        print(f'[今日必读] {top_story["title"][:30]}...')

    # 4. 格式化 & 保存
    content = format_daily(today, all_news, prefs, top_story)
    save_daily(news_dir, today, content)

    # 4. 更新索引
    counts = {cat: len(items) for cat, items in all_news.items()}
    update_index(news_dir, today, counts)

    print('[完成]')


if __name__ == '__main__':
    main()
