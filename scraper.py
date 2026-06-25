#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 喜讯采集脚本
采集多平台 AI 相关热讯，计算热度分，输出 data.json
"""

import json
import re
import asyncio
import aiohttp
from datetime import datetime, timezone
from pathlib import Path

# 关键词过滤（标题或内容包含这些词才收录）
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "large language model", "gpt", "chatgpt", "claude", "gemini",
    "openai", "anthropic", "google deepmind", "meta ai", "mistral",
    "stable diffusion", "midjourney", "sora", "runway",
    "nvidia", "gpu", "transformer", "neural",
    "agent", "copilot", "rag", "fine-tune", "rlhf",
    "多模态", "大模型", "人工智能", "深度学习", "生成式",
]

OUTPUT = Path(__file__).parent / "data.json"

# ═══════════════════════════════════════════════════════════════════════════════
# 数据源采集
# ═══════════════════════════════════════════════════════════════════════════════

async def fetch_hackernews(session: aiohttp.ClientSession) -> list:
    """从 HackerNews 获取 AI 相关热帖"""
    results = []
    try:
        # 获取 top 500 故事 ID
        async with session.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=aiohttp.ClientTimeout(total=15)
        ) as resp:
            story_ids = await resp.json()

        # 取前 100 个详情
        tasks = []
        for sid in story_ids[:100]:
            tasks.append(fetch_hn_story(session, sid))
        stories = await asyncio.gather(*tasks)

        for s in stories:
            if not s:
                continue
            title = s.get("title", "").lower()
            if not any(kw in title for kw in AI_KEYWORDS):
                continue
            score = s.get("score", 0)
            comments = s.get("descendants", 0)
            results.append({
                "title": s["title"],
                "source": "HackerNews",
                "url": s.get("url") or f"https://news.ycombinator.com/item?id={s['id']}",
                "category": categorize(title),
                "score": round(min(100, (score + comments * 3) / 50), 1),
                "trend": "up" if score > 100 else "down",
                "hot": score,
                "comments": comments,
                "time": datetime.fromtimestamp(s.get("time", 0), tz=timezone.utc).isoformat(),
            })
    except Exception as e:
        print(f"[HackerNews] 采集失败: {e}")
    return results


async def fetch_hn_story(session, sid):
    try:
        async with session.get(
            f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
            timeout=aiohttp.ClientTimeout(total=10)
        ) as resp:
            return await resp.json()
    except:
        return None


async def fetch_reddit(session: aiohttp.ClientSession) -> list:
    """从 Reddit r/artificial 获取热帖"""
    results = []
    try:
        headers = {"User-Agent": "AI-News-Hub/1.0"}
        async with session.get(
            "https://www.reddit.com/r/artificial/hot.json?limit=50",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=15)
        ) as resp:
            data = await resp.json()

        for post in data.get("data", {}).get("children", []):
            p = post["data"]
            title = p.get("title", "").lower()
            score = p.get("score", 0)
            comments = p.get("num_comments", 0)
            results.append({
                "title": p["title"],
                "source": "Reddit",
                "url": f"https://reddit.com{p.get('permalink', '')}",
                "category": categorize(title),
                "score": round(min(100, (score + comments * 2) / 80), 1),
                "trend": "up" if score > 50 else "down",
                "hot": score,
                "comments": comments,
                "time": datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc).isoformat(),
            })
    except Exception as e:
        print(f"[Reddit] 采集失败: {e}")
    return results


async def fetch_github(session: aiohttp.ClientSession) -> list:
    """从 GitHub Trending 获取 AI 相关仓库"""
    results = []
    try:
        # GitHub Search API: 最近一周创建的 AI 相关仓库，按 stars 排序
        async with session.get(
            "https://api.github.com/search/repositories",
            params={
                "q": "AI OR LLM OR chatbot OR diffusion created:>" + (
                    datetime.now().strftime("%Y-%m-%d")
                ),
                "sort": "stars",
                "order": "desc",
                "per_page": "30",
            },
            timeout=aiohttp.ClientTimeout(total=15)
        ) as resp:
            data = await resp.json()

        for repo in data.get("items", []):
            name = repo.get("full_name", "")
            desc = repo.get("description") or ""
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            results.append({
                "title": f"GitHub 热榜: {name} - {desc[:80]}",
                "source": "GitHub",
                "url": repo.get("html_url", ""),
                "category": categorize((name + " " + desc).lower()),
                "score": round(min(100, stars / 100 + forks / 30), 1),
                "trend": "up" if stars > 100 else "down",
                "hot": stars,
                "comments": forks,
                "time": repo.get("created_at", datetime.now().isoformat()),
            })
    except Exception as e:
        print(f"[GitHub] 采集失败: {e}")
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 分类 & 排序
# ═══════════════════════════════════════════════════════════════════════════════

def categorize(text: str) -> str:
    text = text.lower()
    if any(w in text for w in ["gpt", "llm", "claude", "gemini", "llama", "model", "大模型", "transformer", "多模态"]):
        return "model"
    if any(w in text for w in ["product", "launch", "release", "update", "app", "tool", "产品", "发布", "上线"]):
        return "product"
    if any(w in text for w in ["research", "paper", "study", "arxiv", "论文", "研究", "突破"]):
        return "research"
    if any(w in text for w in ["funding", "invest", "million", "billion", "融资", "投资", "收购", "并购"]):
        return "invest"
    if any(w in text for w in ["policy", "regulation", "law", "ban", "法案", "政策", "监管", "管制"]):
        return "policy"
    return "product"


def merge_and_rank(*sources) -> list:
    """合并多源数据，去重，按热度排序，取 Top 50"""
    seen = set()
    merged = []

    for items in sources:
        for item in items:
            key = item["title"][:60]
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)

    # 按热度分排序
    merged.sort(key=lambda x: x["score"], reverse=True)

    # 重新赋值排名
    for i, item in enumerate(merged[:50], 1):
        item["rank"] = i

    return merged[:50]


# ═══════════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════════
async def main():
    print("=" * 50)
    print("  AI 喜讯采集脚本")
    print("=" * 50)

    async with aiohttp.ClientSession() as session:
        print("[步骤] 采集 HackerNews...")
        hn = await fetch_hackernews(session)
        print(f"[完成] HackerNews: {len(hn)} 条")

        print("[步骤] 采集 Reddit...")
        rd = await fetch_reddit(session)
        print(f"[完成] Reddit: {len(rd)} 条")

        print("[步骤] 采集 GitHub...")
        gh = await fetch_github(session)
        print(f"[完成] GitHub: {len(gh)} 条")

    print("[步骤] 合并排序...")
    top50 = merge_and_rank(hn, rd, gh)
    print(f"[完成] 最终 Top 50 已生成")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(top50, f, ensure_ascii=False, indent=2)

    print(f"[完成] 已保存: {OUTPUT}")
    print(f"[统计] 模型: {sum(1 for x in top50 if x['category']=='model')} | "
          f"产品: {sum(1 for x in top50 if x['category']=='product')} | "
          f"研究: {sum(1 for x in top50 if x['category']=='research')} | "
          f"投资: {sum(1 for x in top50 if x['category']=='invest')} | "
          f"政策: {sum(1 for x in top50 if x['category']=='policy')}")


if __name__ == "__main__":
    asyncio.run(main())
