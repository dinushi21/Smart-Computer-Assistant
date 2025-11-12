
from typing import List, Dict, Any
import os, requests, json

def tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Return structured answers: [{'title': str, 'url': str, 'summary': str}]"""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        # Fallback demo: return a predictable structure with a 'source' field.
        return [{
            'title': 'Demo Result',
            'url': 'https://example.com',
            'summary': f'No API key set. Would search for: {query}',
            'source': 'demo'
        }]
    payload = {
        'api_key': api_key,
        'query': query,
        'max_results': max_results,
        'include_domains': [],
        'search_depth': 'advanced'
    }
    resp = requests.post(
        'https://api.tavily.com/search',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payload)
    )
    resp.raise_for_status()
    data = resp.json()
    # Normalize to a predictable structure
    results = []
    for r in data.get('results', []):
        results.append({
            'title': r.get('title'),
            'url': r.get('url'),
            'summary': r.get('content') or r.get('snippet') or '',
            'source': 'tavily'
        })
    return results
