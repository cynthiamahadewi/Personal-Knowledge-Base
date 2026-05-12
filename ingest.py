"""
ingest.py — Collect sources into raw/ directory.
Supports: URLs (via requests + readability), plain text, and .txt/.md files.
Usage:
    python ingest.py --url https://arxiv.org/abs/1706.03762
    python ingest.py --text "My note about transformers..." --title "transformers_note"
    python ingest.py --file path/to/article.txt
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:60]


def save_source(title: str, content: str, source_url: str = "", source_type: str = "text"):
    slug = slugify(title)
    uid = hashlib.md5(content.encode()).hexdigest()[:8]
    filename = f"{slug}_{uid}.json"
    path = RAW_DIR / filename

    doc = {
        "title": title,
        "content": content,
        "source_url": source_url,
        "source_type": source_type,
        "ingested_at": datetime.utcnow().isoformat(),
        "uid": uid,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    print(f"[ingest] Saved → {filename}")
    return filename


def ingest_url(url: str):
    try:
        import requests
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text_parts = []
                self.skip_tags = {"script", "style", "nav", "footer", "header"}
                self.current_skip = 0

            def handle_starttag(self, tag, attrs):
                if tag in self.skip_tags:
                    self.current_skip += 1

            def handle_endtag(self, tag):
                if tag in self.skip_tags:
                    self.current_skip = max(0, self.current_skip - 1)

            def handle_data(self, data):
                if self.current_skip == 0:
                    stripped = data.strip()
                    if stripped:
                        self.text_parts.append(stripped)

        headers = {"User-Agent": "Mozilla/5.0 (compatible; KnowledgeBase/1.0)"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        # Extract title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else url

        extractor = TextExtractor()
        extractor.feed(resp.text)
        content = "\n".join(extractor.text_parts)
        content = re.sub(r"\n{3,}", "\n\n", content)

        return save_source(title, content, source_url=url, source_type="url")

    except ImportError:
        print("[ingest] 'requests' not installed. Run: pip install requests")
        sys.exit(1)
    except Exception as e:
        print(f"[ingest] Failed to fetch URL: {e}")
        sys.exit(1)


def ingest_text(text: str, title: str):
    return save_source(title, text, source_type="text")


def ingest_file(filepath: str):
    path = Path(filepath)
    if not path.exists():
        print(f"[ingest] File not found: {filepath}")
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    return save_source(path.stem, content, source_url=str(path.resolve()), source_type="file")


def list_raw():
    docs = sorted(RAW_DIR.glob("*.json"))
    if not docs:
        print("[ingest] No sources ingested yet.")
        return
    print(f"\n{'─'*60}")
    print(f"  {'TITLE':<35} {'TYPE':<8} {'DATE'}")
    print(f"{'─'*60}")
    for doc_path in docs:
        with open(doc_path) as f:
            doc = json.load(f)
        date = doc.get("ingested_at", "")[:10]
        print(f"  {doc['title'][:35]:<35} {doc['source_type']:<8} {date}")
    print(f"{'─'*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest sources into the knowledge base.")
    parser.add_argument("--url", help="URL to fetch and ingest")
    parser.add_argument("--text", help="Raw text to ingest")
    parser.add_argument("--title", help="Title for --text ingestion", default="untitled")
    parser.add_argument("--file", help="Path to a .txt or .md file")
    parser.add_argument("--list", action="store_true", help="List all ingested sources")
    args = parser.parse_args()

    if args.list:
        list_raw()
    elif args.url:
        ingest_url(args.url)
    elif args.text:
        ingest_text(args.text, args.title)
    elif args.file:
        ingest_file(args.file)
    else:
        parser.print_help()
