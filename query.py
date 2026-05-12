"""
query.py — Ask questions against the compiled wiki.
Usage:
    python query.py "What is attention mechanism?"
    python query.py "Compare transformers and RNNs" --save
    python query.py --interactive
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path(__file__).parent / "wiki"
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"


def call_claude(system: str, messages: list, max_tokens: int = 2000) -> str:
    try:
        import urllib.request
        payload = json.dumps({
            "model": MODEL,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
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
        print(f"[query] Claude API error: {e}")
        raise


def load_wiki_context() -> str:
    """Load all wiki articles into a context string."""
    articles = sorted(WIKI_DIR.glob("*.md"))
    if not articles:
        return ""

    parts = []
    for p in articles:
        content = p.read_text(encoding="utf-8")
        parts.append(f"=== FILE: {p.name} ===\n{content}\n")

    return "\n".join(parts)


def build_system_prompt(wiki_context: str) -> str:
    return f"""You are an AI/ML knowledge base assistant. You have access to a personal wiki containing research notes and articles on AI and machine learning topics.

Use ONLY the wiki content below to answer questions. If the wiki doesn't contain enough information, say so clearly and suggest what topics might help.

When answering:
- Be precise and educational
- Reference specific wiki articles using [[article_name]] syntax
- Suggest follow-up questions at the end
- If asked to compare concepts, use a clear structure

=== WIKI CONTENTS ===
{wiki_context}
=== END WIKI ==="""


def query(question: str, save: bool = False, history: list = None) -> str:
    wiki_context = load_wiki_context()

    if not wiki_context:
        print("[query] No wiki articles found. Run compile_wiki.py first.")
        return ""

    system = build_system_prompt(wiki_context)
    messages = history or []
    messages = messages + [{"role": "user", "content": question}]

    print(f"\n[query] Asking: {question}\n{'─'*60}")
    try:
        answer = call_claude(system, messages, max_tokens=2000)
        print(answer)

        if save:
            slug = re.sub(r"[^\w]+", "_", question[:40]).strip("_")
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            out_path = OUTPUTS_DIR / f"{ts}_{slug}.md"
            content = f"# Q: {question}\n\n*Generated: {datetime.utcnow().isoformat()}*\n\n---\n\n{answer}"
            out_path.write_text(content, encoding="utf-8")
            print(f"\n[query] Saved → outputs/{out_path.name}")

        return answer
    except Exception as e:
        print(f"[query] Error: {e}")
        return ""


def interactive_mode():
    print("\n╔══════════════════════════════════════╗")
    print("║   AI/ML Knowledge Base — Q&A Mode   ║")
    print("╚══════════════════════════════════════╝")
    print("Type your question, or 'quit' to exit, 'save' to toggle saving answers.\n")

    history = []
    save_answers = False

    while True:
        try:
            question = input("❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[query] Goodbye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("[query] Goodbye!")
            break
        if question.lower() == "save":
            save_answers = not save_answers
            print(f"[query] Auto-save {'ON' if save_answers else 'OFF'}")
            continue

        answer = query(question, save=save_answers, history=history)
        if answer:
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})
            # keep last 6 turns to avoid context overflow
            history = history[-12:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the AI/ML knowledge base wiki.")
    parser.add_argument("question", nargs="?", help="Question to ask")
    parser.add_argument("--save", action="store_true", help="Save answer to outputs/")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive Q&A mode")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.question:
        query(args.question, save=args.save)
    else:
        parser.print_help()