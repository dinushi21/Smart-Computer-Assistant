from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from .agentic_search import tavily_search
from .hitl import human_review
from .persistence import get_checkpointer


class AgentState(TypedDict):
    question: str
    findings: List[Dict[str, Any]]
    draft: str
    approved: bool


def node_search(state: AgentState) -> AgentState:
    results = tavily_search(state['question'], max_results=5)
    state['findings'] = results
    return state


def node_draft(state: AgentState) -> AgentState:
    bullets = '\n'.join(f"- {r['title']}: {r['summary'][:160]}" for r in state.get('findings', []))
    state['draft'] = (
        "\n## Answer\n\nBased on research:\n"
        f"{bullets}\n\n(Expand me with an LLM for better prose.)"
    )
    return state


def node_critique(state: AgentState) -> AgentState:
    draft = state.get('draft', '')
    notes: List[str] = []

    if len(draft) < 400:
        notes.append("Draft is short; expand analysis and add 2-3 citations.")
    if "##" not in draft:
        notes.append("Add section headings (##) for structure.")
    if "Conclusion" not in draft:
        notes.append("Consider adding a short conclusion paragraph.")

    if notes:
        state['draft'] += "\n\n### Critique Notes\n" + "\n".join(f"- {n}" for n in notes)

    return state


def node_hitl(state: AgentState) -> AgentState:
    reviewed = human_review({'draft': state.get('draft', ''), 'findings': state.get('findings', [])})
    state['approved'] = reviewed.get('approved', False)
    return state


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node('search', node_search)
    graph.add_node('draft', node_draft)
    graph.add_node('critique', node_critique)
    graph.add_node('hitl', node_hitl)

    graph.add_edge(START, 'search')
    graph.add_edge('search', 'draft')
    graph.add_edge('draft', 'critique')
    graph.add_edge('critique', 'hitl')
    graph.add_edge('hitl', END)

    checkpointer = get_checkpointer()
    return graph.compile(checkpointer=checkpointer)
