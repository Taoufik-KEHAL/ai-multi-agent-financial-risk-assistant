from graph.state import AgentState

from config.llm import get_llm
from tools.prompt_loader import load_prompt


# Initialisation du modèle
model = get_llm()
EVALUATOR_PROMPT = load_prompt("evaluator.txt")


def evaluator_agent(state: AgentState) -> AgentState:
    """
    Agent évaluateur :
    combine les analyses financières et conformité
    puis génère une décision finale.
    """

    financial_analysis = state["financial_analysis"]

    conformite_analysis = state["conformite_analysis"]

    prompt = EVALUATOR_PROMPT.format(
        financial_analysis=financial_analysis,
        conformite_analysis=conformite_analysis,
    )

    response = model.invoke(prompt)

    final_answer = response.content
    final_answer_lower = final_answer.lower()

    if "niveau de risque retenu : élevé" in final_answer_lower:
        state["risk_level"] = "élevé"
    elif "niveau de risque retenu : moyen" in final_answer_lower:
        state["risk_level"] = "moyen"
    elif "niveau de risque retenu : faible" in final_answer_lower:
        state["risk_level"] = "faible"

    print("[EVALUATOR AGENT] Décision finale générée")

    state["decision_draft"] = final_answer
    state["final_answer"] = final_answer

    return state
