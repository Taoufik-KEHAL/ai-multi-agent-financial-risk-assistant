from typing import List, NotRequired, TypedDict


class AgentState(TypedDict):
    question: str
    route: str
    financial_analysis: str
    conformite_analysis: str
    risk_level: str
    final_answer: str
    decision_draft: NotRequired[str]
    documents: List[str]
    human_validation: str
    is_validated: bool
    human_decision: NotRequired[str]
    human_comment: NotRequired[str]
    allow_console_validation: NotRequired[bool]
