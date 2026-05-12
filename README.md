# INDENG 231 Project 2 — AI/ML Personal Knowledge Base

A system that uses an LLM to create and maintain a personal knowledge base on AI/ML topics.
Inspired by Andrej Karpathy's workflow: collect sources → compile wiki → query.

---

## System Architecture

```
sources (URLs, text, notes)
        │
        ▼
   [ ingest.py ]  →  raw/  (JSON docs)
        │
        ▼
[ compile_wiki.py ]  →  wiki/  (linked .md files)
  (Claude API)               │
        │                    └── INDEX.md (master index)
        ▼
   [ query.py ]  ←→  Claude API (Q&A over wiki)
        │
        ▼
  outputs/  (saved answers as .md)
```

---

## Quickstart

### 1. Install dependencies
```bash
pip install requests   # for URL fetching
```

No other dependencies — uses Python stdlib + Claude API.

### 2. Set your API key
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add to a `.env` file and source it.

### 3. Seed starter articles
```bash
python seed.py
```
This adds 6 foundational AI/ML articles to `raw/`:
- Transformer Architecture
- Attention Mechanism
- Large Language Models
- Gradient Descent & Optimization
- Convolutional Neural Networks
- Reinforcement Learning Fundamentals

### 4. Add your own sources
```bash
# Fetch a URL
python ingest.py --url https://arxiv.org/abs/1706.03762

# Paste text
python ingest.py --text "My notes on diffusion models..." --title "diffusion_notes"

# Load a file
python ingest.py --file my_notes.txt

# List all sources
python ingest.py --list
```

### 5. Compile the wiki
```bash
python compile_wiki.py          # compile new/updated sources only
python compile_wiki.py --rebuild  # recompile everything
python compile_wiki.py --index    # regenerate INDEX.md only
```
This uses Claude to convert each raw source into a structured `.md` file in `wiki/`.

### 6. Query the knowledge base
```bash
# Single question
python query.py "What is the attention mechanism?"

# Save answer to outputs/
python query.py "Compare Transformers and CNNs" --save

# Interactive mode (multi-turn conversation)
python query.py --interactive
```

### 7. Web UI
Open `kb_ui.html` in a browser for a visual interface with all three steps integrated.

---

## Project Structure

```
ai_kb/
├── ingest.py          # Collect sources into raw/
├── compile_wiki.py    # Compile raw/ → wiki/ using Claude
├── query.py           # Q&A over the wiki using Claude
├── seed.py            # Load starter AI/ML articles
├── raw/               # Ingested source documents (JSON)
├── wiki/              # Compiled wiki articles (Markdown)
│   └── INDEX.md       # Auto-generated master index
└── outputs/           # Saved Q&A answers (Markdown)
```

---

## Design Decisions

**Why JSON for raw sources?**
Structured metadata (title, source URL, date, UID) alongside content makes it easy to track what's been compiled and detect changes.

**Why Markdown for wiki?**
Plain Markdown is human-readable, LLM-friendly, and compatible with tools like Obsidian (as recommended by Karpathy). `[[WikiLink]]` syntax creates a navigable graph.

**Incremental compilation**
A `.compile_state.json` file tracks which source UIDs have been compiled, so re-running only processes new/changed sources rather than re-calling the API for everything.

**Multi-turn Q&A**
The query module maintains conversation history (last 6 turns) so follow-up questions work naturally. History is trimmed to avoid context overflow.

**No RAG needed at small scale**
At <100 articles, all wiki content fits in Claude's context window directly — no vector DB or chunking needed. This matches Karpathy's observation that the LLM handles "auto-maintaining index files" well at small scale.

---

## Knowledge Topic: AI / Machine Learning

The knowledge base covers foundational and frontier AI/ML topics:
- Model architectures (Transformers, CNNs, RNNs)
- Core algorithms (attention, gradient descent, backprop)
- Large language models and training pipelines
- Reinforcement learning
- Any papers/articles added via ingest.py
