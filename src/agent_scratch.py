
from typing import Dict, Any, List, Callable
import os
from tenacity import retry, wait_exponential, stop_after_attempt

try:
    from openai import OpenAI
    _client = OpenAI()
    _MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
except Exception:
    _client = None
    _MODEL = None

Tool = Callable[[str], str]

class ScratchAgent:
    def __init__(self, tools: Dict[str, Tool]):
        self.tools = tools

    @retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(3))
    def llm(self, prompt: str) -> str:
        if not _client or not _MODEL:
            return 'LLM not configured. Set OPENAI_API_KEY and OPENAI_MODEL.'
        resp = _client.chat.completions.create(
            model=_MODEL,
            messages=[{'role': 'system', 'content': 'You are a helpful agent.'},
                      {'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content

    def run(self, task: str) -> str:
        """Very small ReAct-style loop: think -> act(tool) -> observe -> answer."""
        plan = self.llm(f"""You can use these tools: {list(self.tools.keys())}.

        Task: {task}

        If a tool is needed, respond with: TOOL:<name> | <input>

        Otherwise, respond with FINAL:<answer>""")
        if plan.startswith('TOOL:'):
            _, rest = plan.split(':', 1)
            name, arg = rest.split('|', 1)
            name = name.strip()
            arg = arg.strip()
            if name not in self.tools:
                return f'Unknown tool: {name}'
            observation = self.tools[name](arg)
            answer = self.llm(f"Tool '{name}' returned:\n{observation}\n\nWrite the final answer.")
            return answer
        if plan.startswith('FINAL:'):
            return plan[len('FINAL:'):].strip()
        return plan
