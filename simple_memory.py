# simple_memory.py
import json
from collections import deque
from typing import Dict, List

class SimpleMemory:
    """A basic, in-memory conversation history system without vector search."""
    def __init__(self, user_id="default", max_history=20):
        self.user_id = user_id
        self.conversation_history = deque(maxlen=max_history)
        self.conversation_turns = 0

    def add_exchange(self, user_input: str, ai_response: str, metadata: Dict = None):
        """Store a conversation turn."""
        exchange = {
            "turn": self.conversation_turns,
            "user": user_input,
            "ai": ai_response,
            "metadata": metadata or {}
        }
        self.conversation_history.append(exchange)
        self.conversation_turns += 1

    def get_context_for_ai(self, window_size: int = 5) -> List[Dict]:
        """Get recent conversation for AI context."""
        recent = list(self.conversation_history)[-window_size:]
        formatted = []
        for exchange in recent:
            formatted.append({"role": "user", "content": exchange["user"]})
            formatted.append({"role": "assistant", "content": exchange["ai"]})
        return formatted

    def search_similar_memories(self, query_text: str, n_results: int = 3):
        """Placeholder function (simple keyword match)."""
        results = []
        query_words = set(query_text.lower().split())
        for exchange in reversed(self.conversation_history):
            text = (exchange["user"] + " " + exchange["ai"]).lower()
            if any(word in text for word in query_words):
                results.append({
                    "document": f"User: {exchange['user']}\nAI: {exchange['ai']}",
                    "metadata": exchange.get("metadata", {})
                })
            if len(results) >= n_results:
                break
        # Return in the format your main script expects
        return {"documents": [r["document"] for r in results],
                "metadatas": [r["metadata"] for r in results],
                "distances": [1.0] * len(results)}