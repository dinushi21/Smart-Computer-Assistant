
from src.agentic_search import tavily_search
from src.langgraph_agent import build_graph


def test_search_structure():
    out = tavily_search('test', max_results=1)
    assert isinstance(out, list)
    assert all('title' in r and 'url' in r and 'summary' in r for r in out)


def test_graph_runs():
    graph = build_graph()
    state = {'question': 'What is LangGraph?', 'findings': [], 'draft': '', 'approved': False}
    out = graph.invoke(state, config={"configurable": {"thread_id": "test"}})
    assert 'draft' in out
    assert isinstance(out.get('approved'), bool)
