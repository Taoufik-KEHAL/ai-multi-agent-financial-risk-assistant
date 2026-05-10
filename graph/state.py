from typing import TypedDict, List


class AgentState(TypedDict):
    question: str
    route: str
    financial_analysis: str
    conformite_analysis: str
    risk_level: str
    final_answer: str
    documents: List[str]