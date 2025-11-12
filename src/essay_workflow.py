
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from .agentic_search import tavily_search
from .hitl import human_review
from .persistence import get_checkpointer

class EssayState(TypedDict):
    topic: str
    sources: List[Dict[str, Any]]
    outline: str
    draft: str
    approved: bool

def node_research(state: EssayState) -> EssayState:
    state['sources'] = tavily_search(state['topic'], max_results=6)
    return state

def node_outline(state: EssayState) -> EssayState:
    pts = [s['title'] for s in state.get('sources', [])][:5]
    state['outline'] = "\n".join([f"1. {p}" for p in pts]) or "1. Introduction\n2. Body\n3. Conclusion"
    return state

def node_draft(state: EssayState) -> EssayState:
    heads = state.get('outline', '').splitlines()
    body = "\n\n".join([f"### {h[3:] if h[:3].isdigit() else h}\nWrite 2-3 paragraphs here." for h in heads if h])
    state['draft'] = body or "Draft not generated."
    return state

def node_review(state: EssayState) -> EssayState:
    reviewed = human_review({'outline': state.get('outline',''), 'draft': state.get('draft','')})
    state['approved'] = reviewed.get('approved', False)
    return state

def build_essay_graph():
    g = StateGraph(EssayState)
    g.add_node('research', node_research)
    g.add_node('outline', node_outline)
    g.add_node('draft', node_draft)
    g.add_node('review', node_review)
    g.add_edge(START, 'research')
    g.add_edge('research', 'outline')
    g.add_edge('outline', 'draft')
    g.add_edge('draft', 'review')
    g.add_edge('review', END)
    return g.compile(checkpointer=get_checkpointer())
