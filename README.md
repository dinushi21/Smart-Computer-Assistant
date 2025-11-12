# Smart Computer Assistant — dinushi
============================================

Build a controllable research-and-writing agent in two ways:
1. From scratch in Python
2. With LangGraph (nodes, edges, and state)

------------------------------------------------------------
Why this project?
------------------------------------------------------------
- Demonstrates agentic search that returns structured findings (not just links)
- Shows persistence (state across threads) using SQLite or DuckDB
- Includes a human-in-the-loop (HITL) review step
- Implements a complete essay-writing workflow:
  research → outline → draft → revise
- Comes with a Typer CLI and smoke tests

------------------------------------------------------------
Quickstart
------------------------------------------------------------
# 1) Create and activate environment
uv venv .venv && source .venv/bin/activate
# or:
python -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt

# 2) Set API keys (edit .env or export manually)
export OPENAI_API_KEY=sk-...            # required for LLM calls
export OPENAI_MODEL=gpt-4o-mini         # optional override
export TAVILY_API_KEY=tvly-...          # optional for real search
export HITL_AUTO_APPROVE=false          # true to skip manual review

# 3) Run CLI
python -m src.cli profile
python -m src.cli search "How did transformers change NLP?"
python -m src.cli essay "The social impact of AI in education"

Tip:
If you don’t have a Tavily key, the search step returns structured “stub” data
so the workflow still runs end-to-end.

------------------------------------------------------------
Project Structure
------------------------------------------------------------
src/
 ├── agent_scratch.py      # From-scratch agent loop with tools
 ├── langgraph_agent.py    # LangGraph implementation (nodes/edges/state)
 ├── agentic_search.py     # Structured search returning normalized JSON
 ├── persistence.py        # SQLite/DuckDB persistence layer
 ├── hitl.py               # Human-in-the-loop approval/edit step
 ├── essay_workflow.py     # High-level essay workflow orchestrator
 ├── cli.py                # Typer CLI entrypoint
tests/
 └── test_basic.py         # Smoke tests
docker/
 └── Dockerfile            # Minimal container image

------------------------------------------------------------
Design Notes
------------------------------------------------------------
- Deterministic runs: central LLM config and seeding
- Typed state: Pydantic models define structured thread state
- Composable tools: search, outline, draft, revise all reusable functions
- Persistence: SQLite by default, switchable to DuckDB via env variable
- Modular architecture: each step can be run or tested independently

------------------------------------------------------------
Roadmap Ideas
------------------------------------------------------------
- Add evaluation with ragas or a custom rubric
- Use a local LLM (Ollama, LM Studio, or vLLM)
- Add vector memory (FAISS/Chroma) for long-running threads
- Build a Streamlit or Gradio web interface
- Integrate rubric scoring or feedback analysis
- Add CI tests and lint checks via GitHub Actions

------------------------------------------------------------
License
------------------------------------------------------------
MIT License (2025) — You are free to use, modify, and share.

