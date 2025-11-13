from typing import Dict


class ChatBot:
def __init__(self):
self.knowledge_base: Dict[str, str] = {
"hello": "Hello! How can I help you today?",
"normal bp": "Typical normal BP is around 120/80 mmHg."
}


def process_query(self, query: str) -> str:
q = query.strip().lower()
if "hello" in q:
return self.knowledge_base["hello"]
for k, v in self.knowledge_base.items():
if k in q:
return v
return "I'm not sure about that. Please consult your healthcare provider."


def add_knowledge(self, question: str, answer: str)