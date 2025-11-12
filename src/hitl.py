
from typing import Dict, Any

def human_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder for Human-In-The-Loop. In production, prompt a UI/user.

    Here we simulate an approval step that could modify content.

    """
    # For now, auto-approve and attach a review note.
    payload.setdefault('reviews', []).append('Auto-approved (demo). Replace with real HITL gate.')
    payload['approved'] = True
    return payload
