# Smart Computer Assistant

Build a controllable research-and-writing agent two ways:
1. From scratch in Python; and
2. With LangGraph's flow-based primitives (nodes, edges, and state).

## Why this repo?
- Demonstrates **agentic search** returning structured answers, not just links.
- Shows **persistence** (state across threads) using a lightweight checkpointer.
- Includes a **human-in-the-loop** review step.
- Implements an **essay-writing workflow** (research -> outline -> draft -> revise).

## Quickstart
```bash
# 1) Create env
uv venv .venv && source .venv/bin/activate  # or: python -m venv .venv
pip install -r requirements.txt

# 2) Set API keys
export OPENAI_API_KEY=...           # or other LLM provider key
export OPENAI_MODEL=gpt-4o-mini     # optional override
export TAVILY_API_KEY=...           # optional: for agentic search

# 3) Run CLI
python -m src.cli profile
python -m src.cli search "How did transformers change NLP?"
python -m src.cli essay "The social impact of AI in education"
```

## Attribution & Ethics

Inspired by learning resources on LangGraph and agentic search. I extended it with a custom search wrapper, SQLite persistence, a HITL gate, CLI, and tests.

## What's inside
- `src/agent_scratch.py` - minimal from-scratch agent loop with tools
- `src/langgraph_agent.py` - LangGraph implementation with nodes/edges and checkpointer
- `src/agentic_search.py` - structured web search returning normalized JSON findings
- `src/persistence.py` - simple SQLite/DuckDB-based persistence + LangGraph checkpointer
- `src/hitl.py` - human-in-the-loop approval/edit step
- `src/essay_workflow.py` - end-to-end essay agent
- `src/cli.py` - Typer CLI to run flows
- `tests/test_basic.py` - smoke tests
- `docker/Dockerfile` - container build

## Roadmap ideas (make it yours)
- Add evaluation with `ragas` or custom rubric scoring.
- Swap in your preferred LLM or add a local LLM via Ollama.
- Add vector memory (FAISS/Chroma) for long-running projects.
- Create a Streamlit/Gradio UI demo.
