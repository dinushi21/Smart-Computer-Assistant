
import typer
from rich import print as rprint
import os
from .agent_scratch import ScratchAgent
from .agentic_search import tavily_search
from .langgraph_agent import build_graph
from .essay_workflow import build_essay_graph

app = typer.Typer(no_args_is_help=True)

@app.command()
def search(q: str):
    """Run agentic search and print structured results."""
    results = tavily_search(q)
    rprint(results)

@app.command()
def scratch(task: str):
    """Run the from-scratch agent on a task."""
    agent = ScratchAgent({'search': lambda q: str(tavily_search(q))})
    out = agent.run(task)
    rprint(out)

@app.command()
def graph(q: str):
    """Run the LangGraph agent."""
    graph = build_graph()
    state = {'question': q, 'findings': [], 'draft': '', 'approved': False}
    out = graph.invoke(state, config={"configurable": {"thread_id": "cli-graph"}})
    rprint(out)

@app.command()
def essay(topic: str):
    """Run the essay-writing workflow."""
    g = build_essay_graph()
    state = {'topic': topic, 'sources': [], 'outline': '', 'draft': '', 'approved': False}
    out = g.invoke(state)
    rprint(out)

@app.command()
def profile():
    """Show project configuration."""
    info = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "db_path": os.getenv("AGENT_DB_PATH", "dinushi_agent.sqlite3"),
        "search": "tavily" if os.getenv("TAVILY_API_KEY") else "demo"
    }
    rprint(info)

if __name__ == '__main__':
    app()
