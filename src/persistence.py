
from typing import Optional, Dict, Any
import sqlite3, json, os, datetime as dt, atexit
from langgraph.checkpoint.sqlite import SqliteSaver

DB_PATH = os.getenv('AGENT_DB_PATH', 'dinushi_agent.sqlite3')
_CHECKPOINTER_CM = None
_CHECKPOINTER = None


def _close_checkpointer():
    global _CHECKPOINTER_CM
    if _CHECKPOINTER_CM is not None:
        _CHECKPOINTER_CM.__exit__(None, None, None)
        _CHECKPOINTER_CM = None


def get_checkpointer():
    global _CHECKPOINTER_CM, _CHECKPOINTER
    if _CHECKPOINTER is None:
        os.makedirs(os.path.dirname(DB_PATH) or '.', exist_ok=True)
        _CHECKPOINTER_CM = SqliteSaver.from_conn_string(DB_PATH)
        _CHECKPOINTER = _CHECKPOINTER_CM.__enter__()
        atexit.register(_close_checkpointer)
    return _CHECKPOINTER

def save_thread_state(thread_id: str, state: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, state TEXT, updated_at TEXT)')
        conn.execute('INSERT OR REPLACE INTO threads (id, state, updated_at) VALUES (?, ?, ?)',
                     (thread_id, json.dumps(state), dt.datetime.utcnow().isoformat()))
        conn.commit()

def load_thread_state(thread_id: str) -> Optional[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, state TEXT, updated_at TEXT)')
        cur = conn.execute('SELECT state FROM threads WHERE id = ?', (thread_id,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None
