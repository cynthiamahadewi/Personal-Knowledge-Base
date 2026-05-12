"""
compile_wiki.py — Use Claude to compile raw/ sources into a linked markdown wiki.
Usage:
    python compile_wiki.py              # compile all new/updated sources
    python compile_wiki.py --rebuild    # recompile everything from scratch
    python compile_wiki.py --index      # regenerate index only
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

RAW_DIR = Path(__file__).parent / "raw"
WIKI_DIR = Path(__file__).parent / "wiki"
WIKI_DIR.mkdir(exist_ok=True)
STATE_FILE = Path(__file__).parent / ".compile_state.json"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"


def call_claude(system: str, user: str, max_tokens: int = 4000) -> str:
    try:
        import urllib.request
        payload = json.dumps({
            "model": MODEL,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }).encode()

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        req = urllib.request.Request(
            ANTHROPIC_API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": api_key,
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except Exception as e:
        print(f"[compile] Claude API error: {e}")
        raise


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"compiled": {}}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_raw_sources() -> list[dict]:
    sources = []
    for p in sorted(RAW_DIR.glob("*.json")):
        with open(p) as f:
            doc = json.load(f)
            doc["_filename"] = p.name
        sources.append(doc)
    return sources


def compile_source(doc: dict) -> str:
    """Ask Claude to turn one raw source into a wiki article."""
    title = doc["title"]
    content = doc["content"][:6000]  # trim to avoid token overflow

    system = """You are a knowledge base compiler for an AI/ML research wiki.
Your job: convert raw source material into a clean, well-structured markdown article.

Rules:
- Write a clear # Title at the top
- Add a short ## Summary (2-3 sentences)
- Use ## sections for key concepts
- Bold important terms on first use
- At the end, add a ## Related Concepts section listing 3-6 related AI/ML topics as [[WikiLinks]]
- Add a ## Tags section with 3-5 lowercase tags like `#neural-networks #transformers`
- Be factual, concise, and educational
- Output ONLY the markdown, no preamble"""

    user = f"""Convert this source into a wiki article:

TITLE: {title}
SOURCE TYPE: {doc.get('source_type', 'text')}
CONTENT:
{content}"""

    return call_claude(system, user, max_tokens=2000)


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "_", text.strip())[:60]


def compile_all(rebuild: bool = False):
    state = load_state()
    sources = load_raw_sources()

    if not sources:
        print("[compile] No sources found in raw/. Run ingest.py first.")
        return

    compiled_articles = []
    for doc in sources:
        uid = doc["uid"]
        filename = slugify(doc["title"]) + ".md"

        if not rebuild and uid in state["compiled"]:
            print(f"[compile] Skipping (already compiled): {doc['title']}")
            article_path = WIKI_DIR / state["compiled"][uid]
            if article_path.exists():
                compiled_articles.append({"title": doc["title"], "file": state["compiled"][uid]})
            continue

        print(f"[compile] Compiling: {doc['title']}...")
        try:
            markdown = compile_source(doc)
            out_path = WIKI_DIR / filename
            out_path.write_text(markdown, encoding="utf-8")
            state["compiled"][uid] = filename
            compiled_articles.append({"title": doc["title"], "file": filename})
            print(f"[compile] ✓ Written → wiki/{filename}")
        except Exception as e:
            print(f"[compile] ✗ Failed: {e}")

    save_state(state)
    build_index(compiled_articles)


def build_index(articles: list[dict] = None):
    """Ask Claude to build a master index linking all wiki articles."""
    if articles is None:
        articles = []
        for p in sorted(WIKI_DIR.glob("*.md")):
            if p.name == "INDEX.md":
                continue
            content = p.read_text(encoding="utf-8")
            # Extract title from first # heading
            m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
            title = m.group(1) if m else p.stem
            articles.append({"title": title, "file": p.name})

    if not articles:
        print("[compile] No articles to index.")
        return

    article_list = "\n".join(f"- [[{a['file'].replace('.md','')}]] — {a['title']}" for a in articles)

    system = """You are a wiki curator. Create a master INDEX.md for an AI/ML knowledge base.
Output ONLY valid markdown, no preamble."""

    user = f"""Create an INDEX.md for this AI/ML knowledge base wiki.
Include:
- A welcoming intro paragraph about the wiki's purpose (AI/ML topics)
- A ## Articles section listing all articles grouped by rough theme (e.g. Foundations, Deep Learning, NLP, etc.)
- A ## How to Use section explaining wiki-link syntax [[article_name]]
- Timestamp: {datetime.utcnow().strftime('%Y-%m-%d')}

Articles:
{article_list}"""

    print("[compile] Building index...")
    try:
        index_md = call_claude(system, user, max_tokens=1500)
        (WIKI_DIR / "INDEX.md").write_text(index_md, encoding="utf-8")
        print("[compile] ✓ INDEX.md updated")
    except Exception as e:
        print(f"[compile] ✗ Index build failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile raw sources into a wiki.")
    parser.add_argument("--rebuild", action="store_true", help="Recompile all sources from scratch")
    parser.add_argument("--index", action="store_true", help="Regenerate index only")
    args = parser.parse_args()

    if args.index:
        build_index()
    else:
        compile_all(rebuild=args.rebuild)